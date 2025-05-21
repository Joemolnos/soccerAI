# SoccerAI Streamlit App – Architektúra (ASCII diagram)

```
+---------------------------------------------------------------+
|                      SoccerAI Streamlit App                   |
+---------------------------------------------------------------+
|                                                               |
|  +-------------------+     +-------------------+              |
|  |    Sidebar        |     |    Main Content   |              |
|  |-------------------|     |-------------------|              |
|  | - App név, logó   |     | - Csapat1 kiválasztás           |
|  | - Leírás          |     | - Csapat2 kiválasztás           |
|  | - API státusz     |     | - Meccs dátuma (date picker)    |
|  |                   |     | - Előrejelzés gomb              |
|  +-------------------+     | - Eredmények:                   |
|                            |   - Győztes/vesztes/döntetlen    |
|                            |   - Under/Over 2.5 gól           |
|                            |   - Statisztikák (opcionális)    |
|                            +-------------------+              |
|                                                               |
+---------------------^-------------------^---------------------+
                      |                   |                      
                      |                   |                      
                      |                   |                      
      +---------------+-------------------+---------------+      
      |                                               |         
      |   Backend/API logika (api.py, utils.py)       |         
      |   - API-Football kommunikáció                 |         
      |   - Csapat ID lekérés, meccskeresés           |         
      |   - Predikció (győztes, under/over)           |         
      |   - Hibakezelés                               |         
      +--------------------------^--------------------+         
                                 |                              
                                 |                              
                        +--------+---------+                   
                        |   API-Football   |                   
                        |   (3rd party)    |                   
                        +------------------+                   
```

**Magyarázat:**
- A felhasználó a Streamlit UI-n keresztül adja meg a csapatokat és a dátumot.
- A backend logika (api.py, utils.py) kommunikál az API-Football szolgáltatással.
- Az eredmények visszakerülnek a fő tartalmi részbe, ahol vizuálisan jelennek meg.
- A sidebar segíti a navigációt és információt ad az app állapotáról.
