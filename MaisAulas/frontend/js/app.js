const API = "http://localhost:5000/api";
const state = { editing: null, entities: {}, current: null };

const configs = {
  student: {
    endpoint: "students", title: "Aluno",
    fields: [
      ["name","Nome","text",true],["email","E-mail","email",true],["class_id","Turma","number",false],["status","Status","select",false,["active","inactive"]]
    ]
  },
  teacher: {
    endpoint: "teachers", title: "Professor",
    fields: [["name","Nome","text",true],["email","E-mail","email",true],["specialty","Especialidade","text",true]]
  },
  class: {
    endpoint: "classes", title: "Turma",
    fields: [["name","Nome","text",true],["grade","Série","text",true],["shift","Turno","select",false,["Manhã","Tarde","Noite"]]]
  },
  subject: {
    endpoint: "subjects", title: "Disciplina",
    fields: [["name","Nome","text",true],["color","Cor","color",false],["teacher_id","Professor","number",false]]
  },
  activity: {
    endpoint: "activities", title: "Atividade",
    fields: [["title","Título","text",true],["description","Descrição","textarea",false],["subject_id","Disciplina","number",true],["class_id","Turma","number",true],["due_date","Data de entrega","date",true],["status","Status","select",false,["pending","done"]],["max_score","Nota máxima","number",false]]
  },
  announcement: {
    endpoint: "announcements", title: "Aviso",
    fields: [["title","Título","text",true],["message","Mensagem","textarea",true],["category","Categoria","text",false]]
  }
};

function esc(v){return String(v ?? "").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]));}
async function api(path="", options={}) {
  const res = await fetch(API + path, {headers: {"Content-Type":"application/json",...(options.headers||{})}, ...options});
  const data = await res.json().catch(()=>({}));
  if(!res.ok) throw new Error(data.error || "Erro na API");
  return data;
}
function toast(msg){const el=document.getElementById("toast");el.textContent=msg;el.classList.add("show");setTimeout(()=>el.classList.remove("show"),2500)}
function openSection(id){
  document.querySelectorAll(".page-section").forEach(x=>x.classList.toggle("active",x.id===id));
  document.querySelectorAll(".nav-item").forEach(x=>x.classList.toggle("active",x.dataset.section===id));
  const titles={dashboard:"Olá, Julia! 👋",students:"Alunos",teachers:"Professores",classes:"Turmas",subjects:"Disciplinas",activities:"Atividades",announcements:"Avisos",reports:"Desempenho"};
  document.getElementById("page-title").textContent=titles[id]||"+Aula";
  if(id==="dashboard") loadDashboard();
  if(id==="students") loadEntity("student");
  if(id==="teachers") loadEntity("teacher");
  if(id==="classes") loadEntity("class");
  if(id==="subjects") loadEntity("subject");
  if(id==="activities") loadActivities(false);
  if(id==="announcements") loadEntity("announcement");
  if(id==="reports") loadReport();
}
document.querySelectorAll(".nav-item").forEach(btn=>btn.addEventListener("click",()=>openSection(btn.dataset.section)));

async function loadDashboard(){
  try{
    const [dash, acts, anns] = await Promise.all([api("/dashboard?student_id=1"), api("/activities?status=pending"), api("/announcements")]);
    document.getElementById("average-score").textContent=String(dash.average_score||0).replace(".",",");
    document.getElementById("pending-list").innerHTML=acts.slice(0,3).map(a=>`<div class="class-row"><span class="subject-icon purple">✓</span><div><b>${esc(a.title)}</b><small>Entrega: ${esc(a.due_date)}</small></div><strong>${esc(a.subject_name||"")}</strong></div>`).join("") || "<p>Sem atividades pendentes.</p>";
    document.getElementById("announcement-list").innerHTML=anns.slice(0,3).map(a=>`<div class="class-row"><span class="subject-icon orange">!</span><div><b>${esc(a.title)}</b><small>${esc(a.category)}</small></div></div>`).join("");
  }catch(e){toast(e.message)}
}

async function loadEntity(type){
  const cfg=configs[type];
  try{
    const data=await api("/"+cfg.endpoint);
    state.entities[type]=data;
    const target=document.getElementById(({student:"students",teacher:"teachers",class:"classes",subject:"subjects",announcement:"announcements"}[type]||type)+"-table");
    renderTable(type,data,target);
  }catch(e){toast("Não foi possível carregar: "+e.message)}
}

function renderTable(type,data,target){
  if(!target) return;
  const columns={
    student:[["name","Nome"],["email","E-mail"],["class_name","Turma"],["status","Status"]],
    teacher:[["name","Nome"],["email","E-mail"],["specialty","Especialidade"]],
    class:[["name","Turma"],["grade","Série"],["shift","Turno"],["student_count","Alunos"]],
    subject:[["name","Disciplina"],["teacher_name","Professor"],["color","Cor"]],
    activity:[["title","Atividade"],["subject_name","Disciplina"],["class_name","Turma"],["due_date","Entrega"],["status","Status"]],
    announcement:[["title","Título"],["category","Categoria"],["published_at","Publicado"]]
  }[type];
  target.innerHTML=`<table class="data-table"><thead><tr>${columns.map(c=>`<th>${c[1]}</th>`).join("")}<th>Ações</th></tr></thead><tbody>${data.map(row=>`<tr>${columns.map(c=>`<td>${esc(row[c[0]])}</td>`).join("")}<td><div class="actions"><button class="action-btn" onclick="editEntity('${type}',${row.id})">Editar</button><button class="action-btn danger" onclick="deleteEntity('${type}',${row.id})">Excluir</button></div></td></tr>`).join("")}</tbody></table>`;
}

async function loadActivities(useFilter){
  try{
    const qs=useFilter?`?search=${encodeURIComponent(document.getElementById("activity-search").value)}&status=${encodeURIComponent(document.getElementById("activity-status").value)}&sort=due_date&direction=asc`:"";
    const data=await api("/activities"+qs);
    state.entities.activity=data;
    renderTable("activity",data,document.getElementById("activities-table"));
  }catch(e){toast(e.message)}
}

async function deleteEntity(type,id){
  if(!confirm("Confirma a exclusão deste registro?")) return;
  try{await api(`/${configs[type].endpoint}/${id}`,{method:"DELETE"});toast("Registro excluído.");openSection(document.querySelector(".nav-item.active").dataset.section)}catch(e){toast(e.message)}
}

function editEntity(type,id){
  const row=state.entities[type].find(x=>x.id===id);
  openForm(type,row);
}

function openForm(type,data=null){
  state.editing=data;
  const cfg=configs[type];
  document.getElementById("modal-title").textContent=(data?"Editar ":"Novo ")+cfg.title;
  const form=document.getElementById("entity-form");
  form.innerHTML=`<div class="form-grid">${cfg.fields.map(([name,label,kind,required,options])=>{
    let input;
    if(kind==="select") input=`<select name="${name}">${options.map(o=>`<option value="${esc(o)}" ${String(data?.[name]??"")===o?"selected":""}>${esc(o)}</option>`).join("")}</select>`;
    else if(kind==="textarea") input=`<textarea name="${name}" rows="4">${esc(data?.[name]??"")}</textarea>`;
    else input=`<input name="${name}" type="${kind}" value="${esc(data?.[name]??"")}" ${required?"required":""}>`;
    return `<div class="field ${kind==="textarea"?"full":""}"><label>${label}</label>${input}</div>`;
  }).join("")}</div><div class="form-actions"><button type="button" class="secondary" onclick="closeModal()">Cancelar</button><button class="primary">Salvar</button></div>`;
  form.onsubmit=async e=>{
    e.preventDefault();
    const fd=new FormData(form), payload={};
    cfg.fields.forEach(([name,,kind])=>{let v=fd.get(name);if(kind==="number"&&v!=="")v=Number(v);if(v!=="")payload[name]=v});
    try{
      await api("/"+cfg.endpoint+(data?"/"+data.id:""),{method:data?"PUT":"POST",body:JSON.stringify(payload)});
      closeModal();toast("Salvo com sucesso.");openSection(document.querySelector(".nav-item.active").dataset.section);
    }catch(err){toast(err.message)}
  };
  document.getElementById("modal").classList.remove("hidden");
}
function closeModal(){document.getElementById("modal").classList.add("hidden");state.editing=null}
async function loadReport(){
  try{
    const rows=await api("/reports/students/1/performance"), r=rows[0]||{};
    document.getElementById("report-card").innerHTML=`<div class="report-stat"><span>Aluno</span><strong>${esc(r.student_name||"—")}</strong></div><div class="report-stat"><span>Atividades concluídas</span><strong>${esc(r.activities_completed||0)}</strong></div><div class="report-stat"><span>Média geral</span><strong>${esc(r.average_score||0)}</strong></div><div class="report-stat"><span>Menor nota</span><strong>${esc(r.lowest_score||0)}</strong></div><div class="report-stat"><span>Maior nota</span><strong>${esc(r.highest_score||0)}</strong></div>`;
  }catch(e){toast(e.message)}
}
loadDashboard();
