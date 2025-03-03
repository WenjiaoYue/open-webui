from google_pse import search_google_pse
import time
 
begin=time.time()
result = search_google_pse(
                "AIzaSyBFl-Yhd0rlndBzvcP9lRlsDB_1lWYHkww",
                "c42164187006d4f5c",
                "哪吒实时片票房和总票房",
                10,
                "",
            )
print(time.time()-begin)
print(result)