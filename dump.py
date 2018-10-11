#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import asyncio,aiohttp,datetime

endpoint_students='https://2018game.picoctf.com/api/stats/scoreboard/student/{}?_=0'
endpoint_global='https://2018game.picoctf.com/api/stats/scoreboard/global/{}?_=0'
c_s=0
c_g=0
data=[]
cookies={
    'token':'Login Credential Removed',
    'flask':'Login Credential Removed'
         }

ranks_students=[]
ranks_global=[]

async def get_data_students(session,i):
    global c_s
    res=await (await session.get(endpoint_students.format(i))).json()
    for j,data in enumerate(res['data']):
        ranks_students.append((j+1+(i-1)*50,data['name'],data['affiliation'],data['score']))
    c_s+=1

async def get_data_global(session,i):
    global c_g
    res=await (await session.get(endpoint_global.format(i))).json()
    for j,data in enumerate(res['data']):
        ranks_global.append((j+1+(i-1)*50,data['name'],data['affiliation'],data['score']))
    c_g+=1


async def main():
    conn=aiohttp.TCPConnector(ssl=False)
    session=aiohttp.ClientSession(connector=conn,cookies=cookies)
    l=[]
    for i in range(1,250):
        l.append(get_data_students(session,i))
    for i in range(1,250):
        l.append(get_data_global(session,i))
        
    fut=asyncio.gather(*l)
    fut.add_done_callback(lambda f:loop.stop())
    asyncio.ensure_future(fut)

        
loop=asyncio.get_event_loop()
asyncio.ensure_future(main())
loop.run_forever()
ranks_global.sort(key=lambda t:t[0])
ranks_students.sort(key=lambda t:t[0])

f=open('global_ranks.tsv','w+')
f.write(f'Dump generated at {datetime.datetime.now().isoformat()}\n')
f.write('Rank\tTeam Name\tSchool\tScore\n')
t=open('global_ranks.txt','w+')
print(f'Dump generated at {datetime.datetime.now().isoformat()}\n',file=t)
print("{:<5}{:<40}{:<50}{:>5}".format('Rank','Team Name','School','Score'),file=t)
print('-'*100,file=t)
for r in ranks_global:
    f.write('\t'.join(map(str,r)))
    f.write('\n')
    print("{:<5}{:<40}{:<50}{:>5}".format(*r),file=t)
    
f.close()
t.close()

f=open('high_school_ranks.tsv','w+')
f.write(f'Dump generated at {datetime.datetime.now().isoformat()}\n')
f.write('Rank\tTeam Name\tSchool\tScore\n')
t=open('high_school_ranks.txt','w+')
print(f'Dump generated at {datetime.datetime.now().isoformat()}\n',file=t)
print("{:<5}{:<40}{:<50}{:>5}".format('Rank','Team Name','School','Score'),file=t)
print('-'*100,file=t)
for r in ranks_students:
    f.write('\t'.join(map(str,r)))
    f.write('\n')
    print("{:<5}{:<40}{:<50}{:>5}".format(*r),file=t)
    
f.close()
t.close()
