from pathlib import Path
import csv
from datetime import datetime
BASE=Path(__file__).parent;OUT=BASE/'output';OUT.mkdir(exist_ok=True)
def date_norm(v):
    for fmt in ('%Y-%m-%d','%Y/%m/%d','%d-%m-%Y'):
        try:return datetime.strptime(v,fmt).strftime('%Y-%m-%d')
        except ValueError:pass
    return ''
with (BASE/'input/customers_dirty.csv').open(newline='',encoding='utf-8') as f: data=list(csv.DictReader(f))
seen=set();clean=[];issues=[]
for i,r in enumerate(data,2):
    key=r['customer_id'].strip().upper()
    if key in seen:issues.append([i,key,'Duplicate customer ID']);continue
    seen.add(key)
    name=' '.join(r['name'].strip().split()).title();email=r['email'].strip().lower()
    city=r['city'].strip().title();dt=date_norm(r['signup_date'].strip())
    if not name:issues.append([i,key,'Missing name'])
    if not email:issues.append([i,key,'Missing email'])
    if not dt:issues.append([i,key,'Invalid date'])
    clean.append([key,name,email,city,dt])
def save(path,cols,data):
    with path.open('w',newline='',encoding='utf-8') as f:w=csv.writer(f);w.writerow(cols);w.writerows(data)
save(OUT/'customers_clean.csv',['customer_id','name','email','city','signup_date'],clean)
save(OUT/'quality_issues.csv',['source_line','customer_id','issue'],issues)
print(f'Input: {len(data)} | Unique: {len(clean)} | QA issues: {len(issues)}')
