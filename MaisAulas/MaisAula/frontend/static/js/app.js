const state = {
    data: { usuarios: [], turmas: [], atividades: [], entregas: [] },
    filtered: {},
    report: { items: [], resumo: {} },
    editing: null
};

const cfg = {
    usuarios: {
        title: 'Usuário',
        fields: [['nome', 'Nome completo', 'text', true], ['email', 'E-mail', 'email', true]],
        cols: [['nome', 'Nome'], ['email', 'E-mail']]
    },
    turmas: {
        title: 'Turma',
        fields: [
            ['nome_turma', 'Nome da turma', 'text', true],
            ['user_id', 'Responsável', 'relation', true, 'usuarios'],
            ['descricao_atividade', 'Descrição', 'text', false]
        ],
        cols: [['nome_turma', 'Turma'], ['usuario_nome', 'Responsável'], ['descricao_atividade', 'Descrição']]
    },
    atividades: {
        title: 'Atividade',
        fields: [
            ['titulo', 'Título', 'text', true],
            ['descricao_atividade', 'Descrição', 'text', false],
            ['turma_id', 'Turma', 'relation', true, 'turmas'],
            ['data_entrega', 'Data de entrega', 'date', true]
        ],
        cols: [['titulo', 'Atividade'], ['turma_nome', 'Turma'], ['data_entrega', 'Entrega']]
    },
    entregas: {
        title: 'Entrega',
        fields: [
            ['data_entrega', 'Data da entrega', 'date', true],
            ['status_entrega', 'Status', 'select', true, ['Pendente', 'Entregue', 'Atrasada']],
            ['atividade_id', 'Atividade', 'relation', true, 'atividades'],
            ['user_id', 'Usuário', 'relation', true, 'usuarios'],
            ['nota', 'Nota (0 a 10)', 'number', false]
        ],
        cols: [
            ['atividade_titulo', 'Atividade'],
            ['usuario_nome', 'Usuário'],
            ['status_entrega', 'Status'],
            ['data_entrega', 'Data'],
            ['nota', 'Nota']
        ]
    }
};

const esc = value => String(value ?? '').replace(/[&<>"']/g, character => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
}[character]));

async function api(path, options = {}) {
    const response = await fetch('/api' + path, {
        headers: { 'Content-Type': 'application/json' },
        ...options
    });

    let data = {};
    try {
        data = await response.json();
    } catch (_) {
        data = {};
    }

    if (!response.ok) {
        throw new Error(data.error || 'Não foi possível concluir a operação.');
    }

    return data;
}

function toast(message) {
    const element = document.querySelector('#toast');
    element.textContent = message;
    element.classList.add('show');
    setTimeout(() => element.classList.remove('show'), 2600);
}

function statusClass(status) {
    if (status === 'Entregue') return 'done';
    if (status === 'Atrasada') return 'late';
    return 'wait';
}

async function loadAll() {
    const resources = Object.keys(state.data);
    const results = await Promise.all(resources.map(resource => api('/' + resource)));
    resources.forEach((resource, index) => {
        state.data[resource] = results[index];
        state.filtered[resource] = results[index];
    });

    renderDashboard();
    fillFilterOptions();
    Object.keys(cfg).forEach(renderTable);
    renderClassCards();
    await Promise.all([
        applyResourceFilter('turmas'),
        applyResourceFilter('atividades'),
        applyResourceFilter('entregas'),
        applyResourceFilter('usuarios'),
        renderReports()
    ]);
}

async function dashboard() {
    const data = await api('/dashboard');
    const labels = [
        ['Usuários', data.usuarios, 'usuarios'],
        ['Turmas', data.turmas, 'turmas'],
        ['Atividades', data.atividades, 'atividades'],
        ['Entregas', data.entregas, 'entregas'],
        ['Pendentes', data.pendentes, 'entregas']
    ];

    document.querySelector('#summary').innerHTML = labels.map(([label, value, page]) => `
        <div class="stat dashboard-stat" data-page="${page}" role="button" tabindex="0">
            <small>${label}</small>
            <strong>${value}</strong>
        </div>
    `).join('');

    const graded = state.data.entregas.filter(item => item.nota !== null && item.nota !== undefined && item.nota !== '');
    const average = graded.length
        ? graded.reduce((sum, item) => sum + Number(item.nota), 0) / graded.length
        : null;

    document.querySelector('#performance-score').textContent = average === null
        ? '—'
        : average.toFixed(1).replace('.', ',');
    document.querySelector('#performance-label').textContent = average === null
        ? 'Aguardando entregas avaliadas'
        : `${graded.length} entrega(s) com nota`;
    document.querySelector('#performance-chart').innerHTML = graded.slice(0, 8).reverse().map(item => `
        <span style="height:${Math.max(8, Math.min(100, Number(item.nota) * 10))}%"></span>
    `).join('') || '<small class="muted">Sem notas para exibir</small>';
}

function renderDashboard() {
    const classes = state.data.turmas.slice(0, 3);
    document.querySelector('#classes-list').innerHTML = classes.length
        ? classes.map((item, index) => `
            <div class="schedule-item">
                <span class="bubble ${['purple', 'green', 'orange'][index % 3]}">▧</span>
                <div><b>${esc(item.nome_turma)}</b><small>${esc(item.usuario_nome || 'Responsável')}</small></div>
                <span class="schedule-time">Turma</span>
            </div>
        `).join('')
        : '<div class="empty">Nenhuma turma cadastrada.</div>';

    const activities = state.data.atividades.slice(0, 3);
    document.querySelector('#activities-list').innerHTML = activities.length
        ? activities.map((item, index) => `
            <div class="activity-item">
                <span class="bubble ${['purple', 'orange', 'green'][index % 3]}">▤</span>
                <div><b>${esc(item.titulo)}</b><small>${esc(item.turma_nome || 'Sem turma')}</small></div>
                <span class="deadline">${esc(item.data_entrega)}</span>
            </div>
        `).join('')
        : '<div class="empty">Nenhuma atividade cadastrada.</div>';

    const deliveries = state.data.entregas.slice(0, 4);
    document.querySelector('#recent-deliveries').innerHTML = deliveries.length
        ? deliveries.map(item => `
            <div class="delivery">
                <span class="bubble blue">✓</span>
                <div><b>${esc(item.atividade_titulo)}</b><small>${esc(item.usuario_nome)}</small></div>
                <span class="status ${statusClass(item.status_entrega)}">${esc(item.status_entrega)}</span>
            </div>
        `).join('')
        : '<div class="empty">Nenhuma entrega cadastrada.</div>';
}

function fillFilterOptions() {
    const responsible = document.querySelector('#turmas-responsavel');
    if (responsible) {
        const selected = responsible.value;
        responsible.innerHTML = '<option value="">Todos os responsáveis</option>' + state.data.usuarios.map(user => `
            <option value="${user.id}">${esc(user.nome)}</option>
        `).join('');
        responsible.value = selected;
    }

    const activity = document.querySelector('#relatorios-atividade');
    if (activity) {
        const selected = activity.value;
        activity.innerHTML = '<option value="">Todas as atividades</option>' + state.data.atividades.map(item => `
            <option value="${item.id}">${esc(item.titulo)}</option>
        `).join('');
        activity.value = selected;
    }
}

function getFiltered(type) {
    return state.filtered[type] ?? state.data[type] ?? [];
}

function renderClassCards() {
    const rows = getFiltered('turmas');
    document.querySelector('#turmas-cards').innerHTML = rows.map(item => `
        <article class="class-card">
            <h3>${esc(item.nome_turma)}</h3>
            <p>${esc(item.descricao_atividade || 'Turma cadastrada na plataforma')}</p>
            <span class="students">Responsável: ${esc(item.usuario_nome || 'Não informado')}</span>
        </article>
    `).join('') || '<div class="panel empty">Nenhuma turma encontrada.</div>';
}

function renderTable(type) {
    const rows = getFiltered(type);
    const config = cfg[type];
    const target = document.querySelector('#' + type + '-table');
    target.innerHTML = `
        <table class="data">
            <thead><tr>${config.cols.map(column => `<th>${column[1]}</th>`).join('')}<th>Ações</th></tr></thead>
            <tbody>
                ${rows.map(item => `
                    <tr>
                        ${config.cols.map(column => `<td>${esc(item[column[0]] ?? '—')}</td>`).join('')}
                        <td>
                            <button class="action" onclick="openForm('${type}', ${item.id})">Editar</button>
                            <button class="action danger" onclick="removeItem('${type}', ${item.id})">Excluir</button>
                        </td>
                    </tr>
                `).join('') || `<tr><td colspan="${config.cols.length + 1}">Nenhum registro encontrado.</td></tr>`}
            </tbody>
        </table>
    `;
}

function queryString(values) {
    const params = new URLSearchParams();
    Object.entries(values).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') params.set(key, value);
    });
    const query = params.toString();
    return query ? '?' + query : '';
}

async function applyResourceFilter(type) {
    const values = {};
    if (type === 'turmas') {
        values.user_id = document.querySelector('#turmas-responsavel').value;
    } else if (type === 'atividades') {
        values.data_inicio = document.querySelector('#atividades-data-inicio').value;
        values.data_fim = document.querySelector('#atividades-data-fim').value;
    } else if (type === 'entregas') {
        values.status = document.querySelector('#entregas-status').value;
        values.data_inicio = document.querySelector('#entregas-data-inicio').value;
        values.data_fim = document.querySelector('#entregas-data-fim').value;
    } else if (type === 'usuarios') {
        values.nome = document.querySelector('#usuarios-nome').value.trim();
    }

    try {
        state.filtered[type] = await api('/' + type + queryString(values));
        renderTable(type);
        if (type === 'turmas') renderClassCards();
    } catch (error) {
        toast(error.message);
    }
}

async function renderReports() {
    const activityId = document.querySelector('#relatorios-atividade')?.value || '';
    try {
        state.report = await api('/relatorios' + queryString({ atividade_id: activityId }));
    } catch (error) {
        toast(error.message);
        return;
    }

    const summary = state.report.resumo;
    const cards = [
        ['Total de entregas', summary.total],
        ['Concluídas', summary.concluidas],
        ['Atrasadas', summary.atrasadas],
        ['Média geral', summary.media === null ? '—' : Number(summary.media).toFixed(1).replace('.', ',')]
    ];
    document.querySelector('#report-cards').innerHTML = cards.map(([label, value]) => `
        <div class="stat"><small>${label}</small><strong>${value}</strong></div>
    `).join('');

    const columns = cfg.entregas.cols;
    document.querySelector('#report-table').innerHTML = `
        <table class="data">
            <thead><tr>${columns.map(column => `<th>${column[1]}</th>`).join('')}</tr></thead>
            <tbody>
                ${state.report.items.map(item => `
                    <tr>${columns.map(column => `<td>${esc(item[column[0]] ?? '—')}</td>`).join('')}</tr>
                `).join('') || `<tr><td colspan="${columns.length}">Nenhuma entrega encontrada.</td></tr>`}
            </tbody>
        </table>
    `;
}

function clearFilters(type) {
    const fields = {
        turmas: ['#turmas-responsavel'],
        atividades: ['#atividades-data-inicio', '#atividades-data-fim'],
        entregas: ['#entregas-status', '#entregas-data-inicio', '#entregas-data-fim'],
        usuarios: ['#usuarios-nome'],
        relatorios: ['#relatorios-atividade']
    }[type] || [];

    fields.forEach(selector => {
        const element = document.querySelector(selector);
        if (element) element.value = '';
    });

    if (type === 'relatorios') {
        renderReports();
    } else {
        applyResourceFilter(type);
    }
}

function bindFilters() {
    const filters = [
        ['turmas-responsavel', 'turmas', 'change'],
        ['atividades-data-inicio', 'atividades', 'change'],
        ['atividades-data-fim', 'atividades', 'change'],
        ['entregas-status', 'entregas', 'change'],
        ['entregas-data-inicio', 'entregas', 'change'],
        ['entregas-data-fim', 'entregas', 'change'],
        ['usuarios-nome', 'usuarios', 'input']
    ];

    filters.forEach(([id, type, eventName]) => {
        const element = document.querySelector('#' + id);
        if (element) element.addEventListener(eventName, () => applyResourceFilter(type));
    });

    document.querySelector('#relatorios-atividade').addEventListener('change', renderReports);
}

function relationOptions(source, current) {
    const rows = state.data[source] || [];
    const labels = { usuarios: 'nome', turmas: 'nome_turma', atividades: 'titulo' };
    return '<option value="">Selecione...</option>' + rows.map(item => `
        <option value="${item.id}" ${Number(current) === Number(item.id) ? 'selected' : ''}>${esc(item[labels[source]])}</option>
    `).join('');
}

function openPage(id) {
    document.querySelectorAll('.page').forEach(page => page.classList.toggle('active', page.id === id));
    document.querySelectorAll('.nav[data-page]').forEach(button => button.classList.toggle('active', button.dataset.page === id));
    if (id === 'dashboard') dashboard();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function bindDashboardLinks() {
    document.querySelectorAll('.dashboard-link[data-page]').forEach(element => {
        element.addEventListener('click', event => {
            if (event.target.closest('a, button')) return;
            openPage(element.dataset.page);
        });
        element.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                openPage(element.dataset.page);
            }
        });
    });

    const summary = document.querySelector('#summary');
    summary.addEventListener('click', event => {
        const card = event.target.closest('.stat[data-page]');
        if (card) openPage(card.dataset.page);
    });
    summary.addEventListener('keydown', event => {
        const card = event.target.closest('.stat[data-page]');
        if (card && (event.key === 'Enter' || event.key === ' ')) {
            event.preventDefault();
            openPage(card.dataset.page);
        }
    });
}

document.querySelectorAll('.nav[data-page]').forEach(button => {
    button.onclick = () => openPage(button.dataset.page);
});

function openForm(type, id = null) {
    const row = id ? state.data[type].find(item => item.id === id) : null;
    state.editing = { type, id };
    document.querySelector('#modal-title').textContent = (row ? 'Editar ' : 'Novo ') + cfg[type].title;

    document.querySelector('#fields').innerHTML = cfg[type].fields.map(([name, label, kind, required, extra]) => {
        let control;
        if (kind === 'select') {
            control = `<select name="${name}" ${required ? 'required' : ''}>${extra.map(option => `
                <option ${row?.[name] === option ? 'selected' : ''}>${option}</option>
            `).join('')}</select>`;
        } else if (kind === 'relation') {
            control = `<select name="${name}" ${required ? 'required' : ''}>${relationOptions(extra, row?.[name])}</select>`;
        } else {
            const constraints = name === 'nota' ? 'min="0" max="10" step="0.1"' : '';
            control = `<input name="${name}" type="${kind}" ${constraints} value="${esc(row?.[name] ?? '')}" ${required ? 'required' : ''}>`;
        }
        return `<div class="field"><label>${label}</label>${control}</div>`;
    }).join('');

    document.querySelector('#modal').classList.remove('hidden');
}

function closeModal() {
    document.querySelector('#modal').classList.add('hidden');
}

document.querySelector('#form').onsubmit = async event => {
    event.preventDefault();
    const { type, id } = state.editing;
    const payload = {};

    for (const [name, , kind] of cfg[type].fields) {
        let value = new FormData(event.target).get(name);
        if ((kind === 'number' || kind === 'relation') && value !== '') value = Number(value);
        if (value !== '') payload[name] = value;
    }

    try {
        await api('/' + type + (id ? '/' + id : ''), {
            method: id ? 'PUT' : 'POST',
            body: JSON.stringify(payload)
        });
        closeModal();
        toast(id ? 'Alterações salvas com sucesso.' : 'Cadastro realizado com sucesso.');
        await refresh();
    } catch (error) {
        toast(error.message);
    }
};

async function removeItem(type, id) {
    if (!confirm('Deseja realmente excluir este registro?')) return;
    try {
        await api('/' + type + '/' + id, { method: 'DELETE' });
        toast('Registro excluído com sucesso.');
        await refresh();
    } catch (error) {
        toast(error.message);
    }
}

async function refresh() {
    try {
        await loadAll();
        await dashboard();
        toast('Dados atualizados.');
    } catch (error) {
        toast(error.message);
    }
}

function loadSettings() {
    let settings = {};
    try {
        settings = JSON.parse(localStorage.getItem('maisAulaSettings') || '{}');
    } catch (_) {
        settings = {};
    }
    document.querySelector('#display-name').value = settings.name || 'Julia';
    document.querySelector('#welcome-message').value = settings.message || 'Tudo pronto para organizar seu dia de aprendizado.';
    applySettings(settings);
}

function applySettings(settings) {
    const name = settings.name || 'Julia';
    document.querySelector('#title').textContent = `Olá, ${name}!`;
    document.querySelector('#subtitle').textContent = settings.message || 'Tudo pronto para organizar seu dia de aprendizado.';
}

document.querySelector('#save-settings').onclick = () => {
    const settings = {
        name: document.querySelector('#display-name').value.trim() || 'Julia',
        message: document.querySelector('#welcome-message').value.trim()
    };
    localStorage.setItem('maisAulaSettings', JSON.stringify(settings));
    applySettings(settings);
    toast('Configurações salvas neste navegador.');
};

document.querySelector('#refresh-button').onclick = refresh;
document.querySelector('#print-report').onclick = () => window.print();
document.querySelector('#exit-button').onclick = () => toast('Sessão encerrada localmente.');

bindDashboardLinks();
bindFilters();
loadSettings();
loadAll().then(dashboard).catch(error => toast(error.message));
