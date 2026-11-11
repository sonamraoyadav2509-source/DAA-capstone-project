import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv, random, time
from pathlib import Path
from algorithms.sorting import merge_sort_parcels
from algorithms.knapsack import knapsack
from algorithms.graph import load_graph, dijkstra
from algorithms.tsp import nearest_neighbor_tsp
from utils import load_parcels
from auth_db import init_db, verify_login, register_user, DEFAULT_USER_ID, DEFAULT_PASSWORD
ROOT=Path(__file__).resolve().parent; DATA=ROOT/'data'
BG='#041020'; PANEL='#0D2B50'; NAV='#061A34'; BLUE='#078BFF'; CYAN='#00F0FF'; WHITE='#F7FCFF'; MUTED='#B8D8F5'; GLOW='#48C8FF'; PANEL2='#123D68'; INPUT='#04172D'; 
class App:
 def __init__(self,root):
  self.root=root;root.title('Mini-Courier Planner | Intelligent Delivery System');root.geometry('1480x900');root.minsize(1120,720);root.configure(bg=BG)
  self.parcels=load_parcels(str(DATA/'parcels.csv'));self.graph,_=load_graph(str(DATA/'deliveries.csv'));self.capacity=15.;self.selected=[];self.route=[];self.distance=0.;self.samples=[];self.style();self.build();self.refresh();self.plan(False)
 def style(self):
  s=ttk.Style();s.theme_use('clam');s.configure('Treeview',background=INPUT,foreground=WHITE,fieldbackground=INPUT,rowheight=31,font=('Segoe UI',10),borderwidth=0);s.configure('Treeview.Heading',background='#0876C9',foreground=WHITE,font=('Segoe UI',10,'bold'),relief='flat');s.map('Treeview',background=[('selected','#087FDB')],foreground=[('selected','#FFFFFF')]);s.map('Treeview.Heading',background=[('active','#00AEEB')])
 def btn(self,p,t,fn,col=BLUE):
  b=tk.Button(p,text=t,command=fn,bg=col,fg='white',activebackground='#00CFFF',activeforeground='white',relief='flat',bd=0,cursor='hand2',padx=16,pady=11,font=('Segoe UI',10,'bold'),highlightthickness=1,highlightbackground=GLOW,highlightcolor=CYAN)
  b.bind('<Enter>',lambda e:b.configure(relief='raised',bd=1));b.bind('<Leave>',lambda e:b.configure(relief='flat',bd=0));return b
 def title(self,p,t,sub=''):
  tk.Label(p,text=t,bg=BG,fg=WHITE,font=('Segoe UI',24,'bold')).pack(anchor='w',pady=(8,3))
  if sub:tk.Label(p,text=sub,bg=BG,fg=MUTED).pack(anchor='w',pady=(0,10))
 def table(self,p,cols,heads,h=10):
  f=tk.Frame(p,bg=PANEL2,highlightbackground=CYAN,highlightthickness=1);tr=ttk.Treeview(f,columns=cols,show='headings',height=h)
  for c,x in zip(cols,heads):tr.heading(c,text=x);tr.column(c,width=100,anchor='center')
  sb=ttk.Scrollbar(f,orient='vertical',command=tr.yview);tr.configure(yscrollcommand=sb.set);tr.pack(side='left',fill='both',expand=True);sb.pack(side='right',fill='y');return f,tr
 def build(self):
  h=tk.Frame(self.root,bg='#08264A',height=105,highlightbackground=CYAN,highlightthickness=1);h.pack(fill='x');h.pack_propagate(False)
  tk.Frame(h,bg=CYAN,height=3).pack(fill='x',side='top')
  brand=tk.Frame(h,bg='#08264A');brand.pack(fill='both',expand=True,padx=24)
  tk.Label(brand,text='⬡',bg='#08264A',fg=CYAN,font=('Segoe UI Symbol',34,'bold')).pack(side='left',padx=(0,14))
  words=tk.Frame(brand,bg='#08264A');words.pack(side='left',anchor='center')
  tk.Label(words,text='MINI-COURIER PLANNER',bg='#08264A',fg=WHITE,font=('Segoe UI',25,'bold')).pack(anchor='w',pady=(14,0))
  tk.Label(words,text='INTELLIGENT DELIVERY & PACKING SYSTEM  |  DESIGN & ANALYSIS OF ALGORITHMS',bg='#08264A',fg='#BDEBFF',font=('Segoe UI',9,'bold')).pack(anchor='w')
  right = tk.Frame(brand, bg='#08264A'); right.pack(side='right', padx=12)
  tk.Label(right,text='✦  PREMIUM LOGISTICS WORKSPACE',bg='#08264A',fg=CYAN,font=('Segoe UI',9,'bold')).pack(anchor='e', pady=(8,4))
  self.btn(right,'↪ Logout',self.logout,'#075B9E').pack(anchor='e')
  body=tk.Frame(self.root,bg=BG);body.pack(fill='both',expand=True,padx=14,pady=12);side=tk.Frame(body,bg=NAV,width=190,highlightbackground='#00BFEF',highlightthickness=1);side.pack(side='left',fill='y',padx=(0,12));side.pack_propagate(False);tk.Label(side,text='WORKSPACE',bg=NAV,fg='#8EDCFF',font=('Segoe UI',9,'bold')).pack(anchor='w',padx=16,pady=(18,12));self.content=tk.Frame(body,bg=BG);self.content.pack(side='left',fill='both',expand=True);self.pages={};self.nav={}
  icons={'Dashboard':'⌂','Add Parcel':'▣','View Parcels':'🚚','Plan Delivery':'🗺','Performance':'▥','Visualize Route':'➜','Reports':'▤','About':'ⓘ'}
  tk.Label(side,text='FLEET VEHICLES',bg=NAV,fg=CYAN,font=('Segoe UI',9,'bold')).pack(anchor='w',padx=16,pady=(0,8))
  for n in ['Dashboard','Add Parcel','View Parcels','Plan Delivery','Performance','Visualize Route','Reports','About']:
   b=tk.Button(side,text='  '+icons[n]+'   '+n,anchor='w',bg=NAV,fg=WHITE,activebackground='#104C7E',activeforeground=CYAN,relief='flat',cursor='hand2',font=('Segoe UI',10,'bold'),padx=10,pady=13,command=lambda x=n:self.show(x),highlightthickness=0);b.pack(fill='x',padx=8,pady=3);self.nav[n]=b;p=tk.Frame(self.content,bg=BG);self.pages[n]=p;self.make(n,p)
  self.status=tk.StringVar(value='Ready.');tk.Label(self.root,textvariable=self.status,bg='#08264A',fg=CYAN,anchor='w',padx=18,pady=10,font=('Segoe UI',9,'bold'),highlightbackground=CYAN,highlightthickness=1).pack(fill='x');self.show('Dashboard')
 def make(self,n,p):
  if n=='Dashboard':
   self.title(p,'Dashboard','Complete courier planning workflow using sorting, dynamic programming and graph algorithms.');cards=tk.Frame(p,bg=BG);cards.pack(fill='x',pady=7);self.kpis={}
   for k,l,c in [('total','Total parcels',CYAN),('selected','Selected parcels',CYAN),('weight','Total weight','#62b4ff'),('value','Total value',GLOW),('distance','Route distance',CYAN)]:
    q=tk.Frame(cards,bg='#12345A',highlightbackground=CYAN,highlightthickness=2,bd=0);q.pack(side='left',fill='both',expand=True,padx=3);tk.Label(q,text=l.upper(),bg=PANEL,fg=MUTED).pack(anchor='w',padx=9,pady=(8,1));v=tk.Label(q,text='—',bg=PANEL,fg=CYAN if c==CYAN else GLOW,font=('Segoe UI',16,'bold'));v.pack(anchor='w',padx=9,pady=(0,8));self.kpis[k]=v
   mid=tk.Frame(p,bg=BG);mid.pack(fill='both',expand=True,pady=7);a=tk.Frame(mid,bg=PANEL,padx=10,pady=10,highlightbackground='#00BFEF',highlightthickness=1);a.pack(side='left',fill='both',expand=True,padx=(0,5));b=tk.Frame(mid,bg=PANEL,padx=14,pady=14,highlightbackground='#00BFEF',highlightthickness=1);b.pack(side='left',fill='both',expand=True,padx=(5,0));tk.Label(a,text='PRIORITIZED PARCELS',bg=PANEL,fg=CYAN,font=('Segoe UI',11,'bold')).pack(anchor='w');f,self.dtree=self.table(a,('id','name','priority','deadline','weight','value','dest'),('ID','Parcel','Priority','Deadline','Kg','Value','To'),9);f.pack(fill='both',expand=True);tk.Label(b,text='DELIVERY ROUTE',bg=PANEL,fg=CYAN,font=('Segoe UI',11,'bold')).pack(anchor='w');self.route_lbl=tk.Label(b,text='',bg=PANEL,fg=WHITE,wraplength=400,justify='left',font=('Segoe UI',13),pady=18);self.route_lbl.pack(anchor='w');tk.Label(b,text='ALGORITHM STATUS',bg=PANEL,fg=CYAN,font=('Segoe UI',11,'bold')).pack(anchor='w');self.alg_lbl=tk.Label(b,text='',bg=PANEL,fg=CYAN,justify='left',font=('Consolas',10),pady=8);self.alg_lbl.pack(anchor='w');r=tk.Frame(p,bg=BG);r.pack(fill='x',pady=7);self.btn(r,'▶ Run Complete Planning',self.plan,BLUE).pack(side='left',padx=3);self.btn(r,'＋ Add Parcel',lambda:self.show('Add Parcel')).pack(side='left',padx=3);self.btn(r,'Visualize Route',lambda:self.show('Visualize Route'),BLUE).pack(side='left',padx=3);self.btn(r,'Generate Report',self.save_report,PANEL2).pack(side='left',padx=3)
  elif n=='Add Parcel':
   self.title(p,'Add New Parcel','Priority 5 is highest. New records are saved to the CSV file.');box=tk.Frame(p,bg=PANEL,padx=20,pady=20);box.pack(anchor='nw',fill='x');self.form={}
   for i,(k,l) in enumerate([('id','Parcel ID'),('name','Parcel name'),('priority','Priority 1–5'),('deadline','Deadline day'),('weight','Weight kg'),('value','Parcel value'),('destination','Destination node A–E')]):tk.Label(box,text=l,bg=PANEL,fg=WHITE).grid(row=i,column=0,sticky='w',pady=7);v=tk.StringVar();self.form[k]=v;tk.Entry(box,textvariable=v,width=32,bg=INPUT,fg=WHITE,insertbackground=WHITE,relief='flat',highlightthickness=1,highlightbackground='#00BFEF').grid(row=i,column=1,padx=10,pady=7,ipady=5)
   self.btn(box,'Save Parcel',self.add,BLUE).grid(row=7,column=1,sticky='w',pady=12)
  elif n=='View Parcels':
   self.title(p,'Parcel Management','Select one or more rows to delete.');r=tk.Frame(p,bg=BG);r.pack(fill='x');self.btn(r,'Refresh',self.refresh).pack(side='left',padx=3);self.btn(r,'Delete Selected',self.delete,'#14518A').pack(side='left',padx=3);f,self.ptree=self.table(p,('id','name','priority','deadline','weight','value','dest'),('ID','Parcel','Priority','Deadline','Weight kg','Value','Destination'),16);f.pack(fill='both',expand=True,pady=8)
  elif n=='Plan Delivery':
   self.title(p,'Delivery Planning','Execute all required algorithms from the capstone assignment.');r=tk.Frame(p,bg=PANEL,padx=12,pady=12);r.pack(fill='x');tk.Label(r,text='Bag capacity (kg)',bg=PANEL,fg=WHITE).pack(side='left');self.cap=tk.StringVar(value='15');tk.Entry(r,textvariable=self.cap,width=9,bg=INPUT,fg=WHITE,insertbackground=WHITE).pack(side='left',padx=8);self.btn(r,'Run Algorithms',self.plan,BLUE).pack(side='left');self.output=tk.Text(p,bg=INPUT,fg=WHITE,relief='flat',font=('Consolas',10),insertbackground=CYAN,highlightthickness=1,highlightbackground='#00BFEF');self.output.pack(fill='both',expand=True,pady=8)
  elif n=='Performance':
   self.title(p,'Performance Analysis','Compare algorithm runtime across increasing parcel input sizes.');self.btn(p,'Run Performance Tests',self.performance,BLUE).pack(anchor='w',pady=7);f,self.perftree=self.table(p,('size','sort','knap'),('Input size','Merge Sort ms','Knapsack ms'),7);f.pack(fill='x');self.note=tk.Label(p,text='Run tests to see results.',bg=BG,fg=MUTED);self.note.pack(anchor='w');self.chart=tk.Canvas(p,bg=INPUT,height=260,highlightthickness=0);self.chart.pack(fill='both',expand=True,pady=8)
  elif n=='Visualize Route':
   self.title(p,'Route Visualization','Road network with highlighted nearest-neighbor tour.');self.routecanvas=tk.Canvas(p,bg=INPUT,height=500,highlightthickness=0);self.routecanvas.pack(fill='both',expand=True,pady=8);self.btn(p,'Refresh Route',self.draw_route,BLUE).pack(anchor='w')
  elif n=='Reports':
   self.title(p,'Reports & Evidence','Save project summary and export parcel data.');self.btn(p,'Save Report (.txt)',self.save_report,BLUE).pack(anchor='w',pady=5);self.btn(p,'Export Parcels (.csv)',self.export).pack(anchor='w',pady=5);self.report=tk.Text(p,bg=INPUT,fg=WHITE,height=20,relief='flat',insertbackground=CYAN,highlightthickness=1,highlightbackground='#00BFEF');self.report.pack(fill='both',expand=True,pady=8)
  else:
   self.title(p,'About Mini-Courier Planner','K.R. Mangalam University | ETCCDA302');tk.Label(p,text='OBJECTIVE\nPrioritize parcels, optimize packing, calculate shortest paths and approximate a delivery tour.\n\nALGORITHMS\nMerge Sort — O(n log n) time, O(n) space.\n0/1 Knapsack DP — O(nC) time and space.\nDijkstra — O((V+E) log V) with a heap.\nNearest Neighbor TSP — heuristic approximation, not guaranteed globally optimal.\nPerformance testing — runtime comparison for increasing inputs.\n\nASSUMPTIONS\nUndirected graph, non-negative distances, valid destination nodes.',bg=PANEL,fg=WHITE,justify='left',anchor='nw',padx=26,pady=26,font=('Segoe UI',12),highlightthickness=1,highlightbackground='#00BFEF').pack(fill='both',expand=True)
 def show(self,n):
  for p in self.pages.values():p.pack_forget()
  self.pages[n].pack(fill='both',expand=True)
  for k,b in self.nav.items():b.configure(bg='#087FCB' if k==n else NAV,fg=CYAN if k==n else WHITE,highlightbackground=CYAN if k==n else '#0B3154',highlightthickness=1 if k==n else 0)
  if n=='Visualize Route':self.draw_route()
  if n=='Reports':self.update_report()
 def logout(self):
  if messagebox.askyesno('Logout','Are you sure you want to logout?'):
   self.root.destroy()
   launch_login()

 def persist(self):
  with open(DATA/'parcels.csv','w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=['id','name','priority','deadline','weight','value','destination']);w.writeheader();w.writerows(self.parcels)
 def add(self):
  try:
   d={k:v.get().strip() for k,v in self.form.items()}
   if any(not x for x in d.values()):raise ValueError('Fill all fields.')
   if any(p['id']==d['id'] for p in self.parcels):raise ValueError('Parcel ID already exists.')
   p={'id':d['id'],'name':d['name'],'priority':int(d['priority']),'deadline':int(d['deadline']),'weight':float(d['weight']),'value':int(d['value']),'destination':d['destination']}
   if not 1<=p['priority']<=5 or p['deadline']<1 or p['weight']<=0 or p['value']<0:raise ValueError('Check priority, deadline, weight and value.')
   if p['destination'] not in self.graph:raise ValueError('Destination is not in graph.')
   self.parcels.append(p);self.persist();self.refresh()
   for v in self.form.values():v.set('')
   self.status.set('Parcel saved.');messagebox.showinfo('Saved','Parcel added to CSV.')
  except ValueError as e:messagebox.showerror('Invalid parcel',str(e))
 def delete(self):
  sel=self.ptree.selection()
  if not sel:messagebox.showwarning('Select row','Select a parcel.');return
  ids={self.ptree.item(i,'values')[0] for i in sel};self.parcels=[p for p in self.parcels if p['id'] not in ids];self.persist();self.refresh();self.status.set('Parcel deleted.')
 def refresh(self):
  ordered=merge_sort_parcels(self.parcels)
  for attr in ('dtree','ptree'):
   tree=getattr(self,attr,None)
   if tree:
    tree.delete(*tree.get_children())
    for p in ordered:tree.insert('','end',values=(p['id'],p['name'],p['priority'],p['deadline'],f"{p['weight']:.2f}",p['value'],p['destination']))
  self.kpis_update()
 def plan(self,show=True):
  try:
   if hasattr(self,'cap'):self.capacity=float(self.cap.get())
   if self.capacity<=0:raise ValueError('Capacity must be positive.')
  except ValueError as e:messagebox.showerror('Capacity',str(e));return
  ordered=merge_sort_parcels(self.parcels);self.selected,weight,value=knapsack(ordered,self.capacity);dest=list(dict.fromkeys(p['destination'] for p in self.selected));self.route,self.distance=nearest_neighbor_tsp(self.graph,'Depot',dest);paths=[]
  for d in dest:
   dist,path=dijkstra(self.graph,'Depot',d);paths.append(f"Depot -> {d}: {' -> '.join(path) if path else 'No path'} ({dist:.2f} km)")
  lines=['MINI-COURIER PLANNER — EXECUTION REPORT','='*55,f'Capacity: {self.capacity:.2f} kg',f'Total parcels: {len(self.parcels)}',f'Selected parcels: {len(self.selected)}',f'Selected weight: {weight:.2f} kg',f'Selected value: {value:.2f}','','SORTED PARCELS (MERGE SORT):']+[f"{p['id']} | {p['name']} | priority={p['priority']} | deadline={p['deadline']}" for p in ordered]+['','SELECTED PARCELS (0/1 KNAPSACK):']+[f"{p['id']} | {p['name']} | {p['weight']:.2f} kg | value={p['value']}" for p in self.selected]+['','DIJKSTRA SHORTEST PATHS:']+paths+['','NEAREST-NEIGHBOR TSP:',' -> '.join(self.route),f'Approximate route distance: {self.distance:.2f} km','Nearest-neighbor is an approximation, not guaranteed globally optimal.']
  if hasattr(self,'output'):self.output.delete('1.0','end');self.output.insert('1.0','\n'.join(lines))
  self.route_lbl.configure(text=' → '.join(self.route)+f'\n\nApproximate distance: {self.distance:.2f} km');self.alg_lbl.configure(text='✓ Merge Sort\n✓ 0/1 Knapsack (DP)\n✓ Dijkstra\n✓ Nearest Neighbor TSP');self.refresh();self.draw_route();self.update_report();self.status.set('Planning completed successfully.')
  if show:messagebox.showinfo('Complete','All algorithms executed successfully.')
 def kpis_update(self):
  if not hasattr(self,'kpis'):return
  vals={'total':len(self.parcels),'selected':len(self.selected),'weight':f"{sum(p['weight'] for p in self.selected):.2f} kg",'value':f"₹ {sum(p['value'] for p in self.selected):,}",'distance':f'{self.distance:.2f} km'}
  for k,v in vals.items():self.kpis[k].configure(text=str(v))
 def draw_route(self):
  if not hasattr(self,'routecanvas'):return
  c=self.routecanvas;c.delete('all');w=max(c.winfo_width(),650);h=max(c.winfo_height(),420);pos={'Depot':(w*.5,h*.78),'A':(w*.18,h*.32),'B':(w*.82,h*.32),'C':(w*.5,h*.15),'D':(w*.18,h*.62),'E':(w*.82,h*.62)}
  for a,ns in self.graph.items():
   for b,d in ns:
    if a<b and a in pos and b in pos:x,y=pos[a];xx,yy=pos[b];c.create_line(x,y,xx,yy,fill='#397EAA',width=2);c.create_text((x+xx)/2,(y+yy)/2-8,text=f'{d:g} km',fill=MUTED)
  for a,b in zip(self.route,self.route[1:]):
   if a in pos and b in pos:c.create_line(*pos[a],*pos[b],fill=CYAN,width=6,arrow='last')
  for n,(x,y) in pos.items():c.create_oval(x-24,y-24,x+24,y+24,fill='#078BFF' if n in self.route else '#183858',outline=CYAN if n in self.route else '#4B8DBB',width=3);c.create_text(x,y,text=n,fill=WHITE,font=('Segoe UI',11,'bold'))
  c.create_text(w/2,h-28,text='Route: '+' → '.join(self.route)+f' | {self.distance:.2f} km',fill=CYAN,font=('Segoe UI',11,'bold'))
 def performance(self):
  random.seed(42);self.rows=[]
  for size in [10,50,100,200,400]:
   a=[{'id':str(i),'name':f'P{i}','priority':random.randint(1,5),'deadline':random.randint(1,30),'weight':round(random.uniform(.1,2),1),'value':random.randint(10,500),'destination':'A'} for i in range(size)];t=time.perf_counter();sdata=merge_sort_parcels(a);s=(time.perf_counter()-t)*1000;t=time.perf_counter();knapsack(sdata,20);k=(time.perf_counter()-t)*1000;self.rows.append((size,s,k))
  self.perftree.delete(*self.perftree.get_children())
  for n,s,k in self.rows:self.perftree.insert('','end',values=(n,f'{s:.4f}',f'{k:.4f}'))
  with open(ROOT/'performance_results.csv','w',newline='',encoding='utf-8') as f:w=csv.writer(f);w.writerow(['input_size','merge_sort_ms','knapsack_ms']);w.writerows(self.rows)
  self.note.configure(text='Runtime saved to performance_results.csv. Timings vary by hardware.');self.draw_chart();self.status.set('Performance tests completed.')
 def draw_chart(self):
  c=self.chart;c.delete('all')
  if not self.rows:return
  w=max(c.winfo_width(),650);h=max(c.winfo_height(),240);l,t,r,b=55,18,w-20,h-40;mx=max(max(x[1],x[2]) for x in self.rows)*1.15 or 1;c.create_line(l,b,r,b,fill=MUTED);c.create_line(l,t,l,b,fill=MUTED)
  for i in range(5):y=b-(b-t)*i/4;c.create_line(l,y,r,y,fill='#1e3853');c.create_text(l-7,y,text=f'{mx*i/4:.1f}',fill=MUTED,anchor='e')
  for i,row in enumerate(self.rows):
   x=l+(r-l)*i/max(1,len(self.rows)-1);c.create_text(x,b+15,text=str(row[0]),fill=WHITE)
   for v,col in [(row[1],CYAN),(row[2],'#078BFF')]:y=b-(b-t)*v/mx;c.create_oval(x-5,y-5,x+5,y+5,fill=col,outline=WHITE,width=1)
 def update_report(self):
  if not hasattr(self,'report'):return
  self.report.delete('1.0','end');self.report.insert('1.0',f"MINI-COURIER PLANNER\n{'='*40}\nParcels: {len(self.parcels)}\nSelected: {len(self.selected)}\nCapacity: {self.capacity:.2f} kg\nWeight: {sum(p['weight'] for p in self.selected):.2f} kg\nValue: {sum(p['value'] for p in self.selected)}\nRoute: {' -> '.join(self.route)}\nDistance: {self.distance:.2f} km\nAlgorithms: Merge Sort, Knapsack DP, Dijkstra, Nearest Neighbor TSP\n")
 def save_report(self):
  self.update_report();path=filedialog.asksaveasfilename(defaultextension='.txt',initialfile='Mini_Courier_Planner_Report.txt',filetypes=[('Text','*.txt')])
  if path:Path(path).write_text(self.report.get('1.0','end'),encoding='utf-8');self.status.set('Report saved.');messagebox.showinfo('Saved','Report saved.')
 def export(self):
  path=filedialog.asksaveasfilename(defaultextension='.csv',initialfile='parcel_export.csv',filetypes=[('CSV','*.csv')])
  if path:
   with open(path,'w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=['id','name','priority','deadline','weight','value','destination']);w.writeheader();w.writerows(self.parcels)
   self.status.set('Parcel CSV exported.')

class LoginWindow:
 def __init__(self, root):
  self.root = root
  root.title('Login | Mini-Courier Planner')
  root.state('zoomed')
  root.resizable(True, True)
  root.configure(bg='#041020')

  outer = tk.Frame(root, bg='#0D2B50', highlightbackground='#00F0FF', highlightthickness=2)
  outer.place(relx=0.5, rely=0.5, anchor='center', width=560, height=660)
  tk.Frame(outer, bg='#00F0FF', height=5).pack(fill='x')

  tk.Label(outer, text='⬡', bg='#0D2B50', fg='#00F0FF',
           font=('Segoe UI Symbol', 42, 'bold')).pack(pady=(15, 0))
  tk.Label(outer, text='MINI-COURIER PLANNER', bg='#0D2B50', fg='#F7FCFF',
           font=('Segoe UI', 21, 'bold')).pack(pady=(2, 3))
  tk.Label(outer, text='INTELLIGENT DELIVERY & PACKING SYSTEM', bg='#0D2B50',
           fg='#48C8FF', font=('Segoe UI', 9, 'bold')).pack()

  tk.Label(outer, text='WELCOME BACK', bg='#0D2B50', fg='#F7FCFF',
           font=('Segoe UI', 17, 'bold')).pack(pady=(20, 4))
  tk.Label(outer, text='Sign in to access your courier workspace', bg='#0D2B50',
           fg='#B8D8F5', font=('Segoe UI', 10)).pack(pady=(0, 15))

  # Do not disable geometry propagation here: it was hiding the form widgets.
  form = tk.Frame(outer, bg='#0D2B50')
  form.pack(fill='x', padx=55)

  tk.Label(form, text='USER ID', bg='#0D2B50', fg='#8EDCFF',
           font=('Segoe UI', 9, 'bold')).pack(anchor='w')
  self.user = tk.StringVar()
  ue = tk.Entry(form, textvariable=self.user, bg='#04172D', fg='#F7FCFF',
                insertbackground='#00F0FF', relief='flat', font=('Segoe UI', 12),
                highlightthickness=1, highlightbackground='#00BFEF')
  ue.pack(fill='x', ipady=9, pady=(5, 12))

  tk.Label(form, text='PASSWORD', bg='#0D2B50', fg='#8EDCFF',
           font=('Segoe UI', 9, 'bold')).pack(anchor='w')
  self.password = tk.StringVar()
  self.visible = tk.BooleanVar(value=False)
  row = tk.Frame(form, bg='#04172D', highlightbackground='#00BFEF', highlightthickness=1)
  row.pack(fill='x', pady=(5, 7))
  self.pe = tk.Entry(row, textvariable=self.password, show='●', bg='#04172D',
                     fg='#F7FCFF', insertbackground='#00F0FF', relief='flat',
                     font=('Segoe UI', 12))
  self.pe.pack(side='left', fill='x', expand=True, ipady=9, padx=8)
  tk.Checkbutton(row, text='Show', variable=self.visible, command=self.toggle,
                 bg='#04172D', fg='#48C8FF', selectcolor='#0D2B50',
                 activebackground='#04172D', activeforeground='#00F0FF').pack(side='right', padx=6)

  self.error = tk.Label(form, text='', bg='#0D2B50', fg='#FF8A9B',
                        font=('Segoe UI', 9, 'bold'))
  self.error.pack(anchor='w', pady=3)

  tk.Button(form, text='SIGN IN  →', command=self.login, bg='#078BFF', fg='white',
            activebackground='#00CFFF', relief='flat', bd=0, cursor='hand2',
            font=('Segoe UI', 11, 'bold'), pady=11,
            highlightthickness=1, highlightbackground='#00F0FF').pack(fill='x', pady=(7, 5))

  tk.Label(form, text='New to Mini-Courier Planner?', bg='#0D2B50',
           fg='#B8D8F5', font=('Segoe UI', 10)).pack(pady=(8, 4))
  tk.Button(form, text='CREATE NEW ACCOUNT', command=self.open_signup,
            bg='#123D68', fg='#00F0FF', activebackground='#075B9E',
            activeforeground='white', relief='flat', bd=0, cursor='hand2',
            font=('Segoe UI', 10, 'bold'), pady=10,
            highlightthickness=1, highlightbackground='#00F0FF').pack(fill='x')

  tk.Label(outer, text='SECURE COURIER MANAGEMENT WORKSPACE', bg='#0D2B50',
           fg='#48C8FF', font=('Segoe UI', 8, 'bold')).pack(pady=(13, 0))
  tk.Label(outer, text='Default Admin: admin  |  Password: Courier@123',
           bg='#0D2B50', fg='#B8D8F5', font=('Segoe UI', 8)).pack(pady=(5, 0))

  ue.focus_set()
  root.bind('<Return>', lambda event: self.login())

 def toggle(self):
  self.pe.configure(show='' if self.visible.get() else '●')

 def open_signup(self):
  SignupWindow(self.root)

 def login(self):
  if not self.user.get().strip() or not self.password.get():
   self.error.configure(text='Enter both User ID and Password.')
   return
  try:
   if verify_login(self.user.get(), self.password.get()):
    self.root.unbind('<Return>')
    self.root.destroy()
    launch_dashboard()
   else:
    self.error.configure(text='Incorrect User ID or Password. Try again.')
  except Exception as exc:
   messagebox.showerror('Login Error', str(exc))


class SignupWindow:
 def __init__(self, parent):
  self.window=tk.Toplevel(parent)
  self.window.title('Create Account | Mini-Courier Planner')
  self.window.configure(bg='#041020')
  self.window.geometry('520x590')
  self.window.resizable(False,False)
  self.window.transient(parent)
  self.window.grab_set()

  card=tk.Frame(self.window,bg='#0D2B50',highlightbackground='#00F0FF',highlightthickness=2)
  card.place(relx=0.5,rely=0.5,anchor='center',width=440,height=530)
  tk.Frame(card,bg='#00F0FF',height=4).pack(fill='x')
  tk.Label(card,text='CREATE ACCOUNT',bg='#0D2B50',fg='#F7FCFF',
           font=('Segoe UI',20,'bold')).pack(pady=(25,5))
  tk.Label(card,text='Join Mini-Courier Planner',bg='#0D2B50',fg='#48C8FF',
           font=('Segoe UI',10)).pack(pady=(0,18))

  form=tk.Frame(card,bg='#0D2B50')
  form.pack(fill='x',padx=35)
  self.name=tk.StringVar()
  self.user=tk.StringVar()
  self.password=tk.StringVar()
  self.confirm=tk.StringVar()

  for label,var,show in [
   ('FULL NAME',self.name,''),
   ('USER ID',self.user,''),
   ('PASSWORD',self.password,'●'),
   ('CONFIRM PASSWORD',self.confirm,'●')
  ]:
   tk.Label(form,text=label,bg='#0D2B50',fg='#8EDCFF',
            font=('Segoe UI',9,'bold')).pack(anchor='w',pady=(7,0))
   tk.Entry(form,textvariable=var,show=show,bg='#04172D',fg='#F7FCFF',
            insertbackground='#00F0FF',relief='flat',font=('Segoe UI',11),
            highlightthickness=1,highlightbackground='#00BFEF').pack(fill='x',ipady=8,pady=(5,4))

  self.message=tk.Label(form,text='',bg='#0D2B50',fg='#FF8A9B',
                        font=('Segoe UI',9,'bold'))
  self.message.pack(anchor='w',pady=4)

  tk.Button(form,text='CREATE ACCOUNT',command=self.create_account,
            bg='#078BFF',fg='white',activebackground='#00CFFF',
            relief='flat',bd=0,cursor='hand2',font=('Segoe UI',10,'bold'),
            pady=12,highlightthickness=1,highlightbackground='#00F0FF').pack(fill='x',pady=(8,6))
  tk.Button(form,text='CLOSE',command=self.window.destroy,bg='#123D68',
            fg='#00F0FF',activebackground='#075B9E',relief='flat',bd=0,
            cursor='hand2',font=('Segoe UI',9,'bold'),pady=9).pack(fill='x')

 def create_account(self):
  name=self.name.get().strip()
  user=self.user.get().strip()
  password=self.password.get()
  confirm=self.confirm.get()

  if not all([name,user,password,confirm]):
   self.message.configure(text='Please fill in all fields.')
   return
  if len(user)<4:
   self.message.configure(text='User ID must be at least 4 characters.')
   return
  if len(password)<8:
   self.message.configure(text='Password must be at least 8 characters.')
   return
  if password != confirm:
   self.message.configure(text='Passwords do not match.')
   return

  try:
   register_user(name,user,password)
   messagebox.showinfo('Account Created','Your account has been created. Please Sign In.')
   self.window.destroy()
  except ValueError as exc:
   self.message.configure(text=str(exc))
  except Exception as exc:
   messagebox.showerror('Sign Up Error',str(exc))


def launch_dashboard():
 root=tk.Tk(); App(root); root.mainloop()
def launch_login():
 init_db(); root=tk.Tk(); LoginWindow(root); root.mainloop()

if __name__=='__main__':
 launch_login()



