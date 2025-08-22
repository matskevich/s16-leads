## Leads Seeders Playbook

### Purpose
Короткий, проверенный временем процесс выбора кандидатов из офлайн-ивентов, их сверки с `s16 space`, пометки `stale` и безопасной итерации следующей десятки.

### Data sources
- `data/export/s16_export_YYYYMMDD_HHMMSS/members.json` — агрегированный список офлайн-ивентов (root: `{ members: [...] }`).
- `s16_space_all_participants.json` — свежий снимок участников `s16 space` (референс).

### Field semantics
- `in_s16_space: bool` — принадлежность к референсной группе на момент последнего снапшота.
- `stale: bool` — помечен как уже рассмотренный (исключать из «next» до истечения срока).
- `stale_set_at: ISO8601` — когда пометили `stale`.
- `stale_until: ISO8601` — до какой даты исключать (по умолчанию 180 дней).

### Golden workflow (операционный)
1) Refresh space snapshot (анти-спам защита активна)
   ```bash
   env PYTHONPATH=. python3 -m src.cli export -1002188344480 \
     --output s16_space_all_participants.json --limit 100000
   ```

2) Sync flags (обновить `in_s16_space` в агрегате)
   - Либо однострочным Python (без сторонних скриптов), либо через существующий utility.
   - Обязательно: перед записью делать backup.

3) Compute next top-10
   - Критерии отбора:
     - НЕ в `s16 space` (`in_s16_space == false`)
     - НЕ активный `stale` (нет `stale_until` в будущем)
   - Сортировка: `offline_cnt` по убыванию, затем `last_offline_at` по убыванию.
   - Вывести превью топ-10 для ручного подтверждения (не помечать автоматически).

4) Mark selected seeders (ровно 10)
   - Помечаем только утвержденные 10:
     - `stale=true`
     - `stale_set_at=now(UTC)`
     - `stale_until=now(UTC)+180d`
     - `stale_reason='seeders-next-top10 <timestamp>'`
   - Сделать backup перед записью.

5) Verify
   - Повторно вывести топ-30 «не в space» с признаком `stale да/нет` и полями `stale_set_at/stale_until`.
   - Сверить, что в топ попали следующие «чистые» кандидаты.

### Safeguards (важные правила)
- Никогда не помечать `stale` больше чем ровно выбранную десятку.
- Если случайно пометили лишних — откатить `stale` для всех, кто не входит в утвержденную 10 (удалить `stale*` поля) и повторить расчет.
- Всегда сохранять `.bak` рядом с целевым JSON.
- Перед каждой итерацией обновлять `s16 space` и синхронизировать `in_s16_space`.

### Typical pitfalls и как их избежать
- «Все в топ-30 стали stale» — причина: пометка без фильтра «ровно 10». Решение: откатить `stale` у лишних, фиксировать только подтвержденную 10.
- Несвежий `s16 space` — перед расчетом всегда делать экспорт свежего снапшота и повторный sync флагов.
- Маппинг по `username` может быть неполным — дополнительно проверяйте по `id`, если он известен в обоих источниках.

### Quick commands (примеры)
- Обновить `s16 space`:
  ```bash
  env PYTHONPATH=. python3 -m src.cli export -1002188344480 \
    --output s16_space_all_participants.json --limit 100000
  ```
- Вывести топ-30 «не в space» с `stale`:
  ```bash
  python3 - <<'PY'
  import json; from datetime import datetime, timezone
  p='data/export/s16_export_20250804_212743/members.json'; d=json.load(open(p));
  m=d['members'] if isinstance(d,dict) else d
  def dt(s):
      try: return datetime.fromisoformat(s)
      except: return None
  rows=[]
  for x in m:
      if x.get('in_s16_space'): continue
      oc=x.get('offline_cnt') or 0
      lo=dt(x.get('last_offline_at')) or datetime(1970,1,1,tzinfo=timezone.utc)
      rows.append((oc, lo, x))
  rows.sort(key=lambda t:(t[0],t[1]), reverse=True)
  for i,(_,__,x) in enumerate(rows[:30],1):
      fs=dt(x.get('first_seen_at')); lo=dt(x.get('last_offline_at'))
      y1=fs.year if fs else '—'; y2=lo.year if lo else '—'
      print(f"{i}) @{x.get('username') or '<no_username>'} ({(x.get('first_name') or '')} {(x.get('last_name') or '')}) - "
            f"{x.get('offline_cnt') or 0} ивентов ({y1}-{y2}) [stale:{'да' if x.get('stale') else 'нет'}]")
  PY
  ```
- Пометить конкретную десятку как `stale` (пример шаблона):
  ```bash
  python3 - <<'PY'
  import json, pathlib, shutil; from datetime import datetime, timedelta, timezone
  P=pathlib.Path('data/export/s16_export_20250804_212743/members.json')
  r=json.load(open(P)); m=r['members'] if isinstance(r,dict) else r
  keep=['sundered','AleksandrAn888','lightmindflight','nina_gavrish','rdegtiarev',
        'peltzer21','pavelshter','katya_zhukovka','OlegoSvetSaharok','RudiTania']
  now=datetime.now(timezone.utc)
  idx={ (u:= (x.get('username') or '')).lower(): x for x in m }
  for u in keep:
      x=idx.get(u.lower());
      if not x: continue
      x['stale']=True; x['stale_set_at']=now.isoformat(timespec='seconds');
      x['stale_until']=(now+timedelta(days=180)).isoformat(timespec='seconds');
      x['stale_reason']=f'seeders-next-top10 {now.isoformat(timespec="seconds")}'
  shutil.copyfile(P, P.with_suffix(P.suffix+'.bak'))
  (json.dump(r if isinstance(r,dict) else m, open(P,'w'), ensure_ascii=False, indent=2))
  PY
  ```

### Notes
- Основной путь — через существующую CLI и функции `GroupManager.get_participants` (анти-спам обертки активны). Отдельные утилиты/скрипты использовать только по необходимости.
- Всегда действуем по принципу: «сначала превью → потом пометка ровно утвержденной 10 → верификация». Риск овермаркировки минимизируется бэкапами и явными фильтрами.
