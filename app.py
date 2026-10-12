import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Academic Leadership",page_icon="🎓",layout="wide")
MODULES={"NAAC Evidence":"naac","NIRF Indicators":"nirf","Compliance":"comp","Governance":"gov","IQAC Evidence":"iqac","Projects":"proj","OBE Mapping":"obe","Research & Patents":"rs","Student Outcomes":"stu","Risk Register":"risk","Communication":"comm","MoUs & Consultancy":"mou","Faculty Workload":"fw","Budget":"bud","To-do":"todo","In Progress":"doing","Completed":"done"}
DEMO={"orgName":"Academic Leadership — Synthetic Demo","kpis":[{"name":"Research Output (sample)","value":"22","status":"ok"},{"name":"Placement % (sample)","value":"80","status":"warn"},{"name":"OBE Mapping % (sample)","value":"90","status":"risk"},{"name":"Patents (sample)","value":"7","status":"ok"}],"iqac":[{"art":"Sample meeting minutes","type":"Minutes","owner":"IQAC","ver":"Draft"}],"risk":[{"risk":"Sample evidence gap","like":"Medium","imp":"High","mit":"Verify","status":"Open"}]}
if "data" not in st.session_state: st.session_state.data=json.loads(json.dumps(DEMO))
st.title("🎓 Academic Leadership Dashboard")
st.caption("IQAC • NAAC • NIRF • Research • OBE • Governance")
with st.sidebar:
    st.header("Workspace")
    upload=st.file_uploader("Import leadership-toolkit JSON",type=["json"])
    if upload is not None:
        identity=(upload.name,upload.size)
        if st.session_state.get("upload_identity")!=identity:
            try:
                if upload.size>10000000: raise ValueError("Maximum size is 10 MB")
                raw=json.loads(upload.getvalue())
                if not isinstance(raw,dict) or not isinstance(raw.get("kpis",[]),list): raise ValueError("Expected object with kpis list")
                st.session_state.data={k:v for k,v in raw.items() if not k.endswith("DataUrl")}
                st.session_state.upload_identity=identity
                st.success("Imported into this session")
            except (ValueError,UnicodeDecodeError) as e: st.error(str(e))
    if st.button("Reset to demo"):
        st.session_state.data=json.loads(json.dumps(DEMO))
        st.session_state.pop("upload_identity",None)
        st.rerun()
    st.warning("No login or permanent database. Do not upload confidential data to a public deployment.")
data=st.session_state.data
st.subheader(str(data.get("orgName","Institution")))
st.info("KPI values are imported or synthetic, not independently verified.")
kpis=[x for x in data.get("kpis",[]) if isinstance(x,dict)]
cols=st.columns(4)
for i,k in enumerate(kpis):
    with cols[i%4]:
        st.metric(str(k.get("name","KPI")),str(k.get("value","—")))
        st.caption("Status: "+str(k.get("status","unclassified")))
overview,records,strategy,exports=st.tabs(["📊 Overview","📁 Module Records","🧭 Strategy & Meetings","⬇️ Export"])
with overview:
    statuses=pd.Series([str(k.get("status","unclassified")) for k in kpis]).value_counts()
    if not statuses.empty: st.bar_chart(statuses)
    st.caption("Status categories are user supplied, not audited ratings.")
    st.dataframe(pd.DataFrame([{"Module":n,"Records":len(data.get(k,[])) if isinstance(data.get(k,[]),list) else 0} for n,k in MODULES.items()]),hide_index=True,use_container_width=True)
with records:
    module=st.selectbox("Select module",list(MODULES))
    key=MODULES[module]
    rows=data.get(key,[])
    if isinstance(rows,list) and rows and all(isinstance(r,dict) for r in rows):
        df=pd.DataFrame(rows).fillna("")
        query=st.text_input("Search")
        if query:
            st.dataframe(df[df.astype(str).apply(lambda s:s.str.contains(query,case=False,regex=False)).any(axis=1)],hide_index=True,use_container_width=True)
        else:
            changed=st.data_editor(df,num_rows="dynamic",use_container_width=True,key="edit_"+key)
            if st.button("Apply edits"):
                data[key]=changed.where(pd.notna(changed),None).to_dict("records")
                st.success("Saved to session; export to retain.")
        st.download_button("Download CSV",df.to_csv(index=False).encode("utf-8-sig"),file_name=key+".csv",mime="text/csv")
    elif isinstance(rows,list) and all(isinstance(r,str) for r in rows):
        value=st.text_area("One item per line",value="\n".join(rows),key="list_"+key)
        if st.button("Apply list edits"): data[key]=[v.strip() for v in value.splitlines() if v.strip()]
    else: st.warning("Module data is not in the expected list format.")
with strategy:
    fields=[("sp-vision","Vision"),("sp-mission","Mission"),("sp-goals","Strategic Goals"),("sp-kpis","Strategic KPIs"),("sp-initiatives","Initiatives"),("sp-policies","Policies"),("mt-title","Meeting Title"),("mt-date","Meeting Date"),("mt-att","Attendees"),("mt-agenda","Agenda"),("mt-decisions","Decisions"),("mt-actions","Actions")]
    for key,label in fields:
        st.text_area(label,value=str(data.get(key,"")),key="field_"+key,height=90)
    if st.button("Apply strategy and meeting edits"):
        for key,_ in fields: data[key]=st.session_state["field_"+key]
        st.success("Updated in current session")
with exports:
    st.download_button("Export updated JSON",json.dumps(data,indent=2,ensure_ascii=False).encode("utf-8"),file_name="academic-leadership-export.json",mime="application/json")
    st.download_button("Export KPI CSV",pd.DataFrame(kpis).to_csv(index=False).encode("utf-8-sig"),file_name="kpis.csv",mime="text/csv")
st.divider()
st.caption("Prototype • Session-only data • No authentication, audit log, or persistent database")
