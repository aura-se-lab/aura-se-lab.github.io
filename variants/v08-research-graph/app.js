/* v08 — Research Graph interactions
 * Vanilla JS. No framework, no graph library.
 * - Hover a node: highlight neighborhood, dim the rest.
 * - Click a node: open the side drawer with that node's metadata.
 */
(function () {
  'use strict';

  // ---------- Node metadata (mirrors the hand-positioned SVG) ----------
  const NODES = {
    // Research avenues
    'ave-explain': {
      kind: 'avenue',
      title: 'Explainability & Interpretability',
      shortLabel: 'Explainability',
      tag: 'AVE.01',
      body: 'Methods that reveal how code models reason — rationales, traces, and tests — so developers can inspect, trust, and debug automation.',
      affordance: 'View research thread'
    },
    'ave-efficient': {
      kind: 'avenue',
      title: 'Efficiency & Resource-Aware Automation',
      shortLabel: 'Efficiency',
      tag: 'AVE.02',
      body: 'Quantization, distillation, and PEFT to deliver low-latency, memory-light, cost-aware automation, measured on real workloads with reproducible metrics.',
      affordance: 'View research thread'
    },
    'ave-multiagent': {
      kind: 'avenue',
      title: 'Multi-Agent LLMs for Software Engineering',
      shortLabel: 'Multi-Agent LLMs',
      tag: 'AVE.03',
      body: 'Role-aligned agents that plan, code, test, and review — coordinated to produce coherent, end-to-end developer assistance.',
      affordance: 'View research thread'
    },
    'ave-neurosym': {
      kind: 'avenue',
      title: 'Neurosymbolic AI for Software Engineering',
      shortLabel: 'Neurosymbolic',
      tag: 'AVE.04',
      body: 'Hybrid pipelines pairing LLMs with program analysis and constraints to produce interpretable, checkable fixes, tests, and designs.',
      affordance: 'View research thread'
    },
    'ave-taskaware': {
      kind: 'avenue',
      title: 'Task-Aware Code Automation',
      shortLabel: 'Task-Aware',
      tag: 'AVE.05 · supporting',
      body: 'From issues, diffs, and traces to concise summaries, TODOs, and plans — models that reduce developer toil with actionable, repo-aware guidance.',
      affordance: 'View research thread'
    },

    // Publications
    'pub-tosem': {
      kind: 'publication',
      title: 'From Triumph to Uncertainty: The Journey of Software Engineering in the AI Era',
      shortLabel: 'From Triumph to Uncertainty',
      authors: 'Mastropaolo, A.; Escobar-Velásquez, C.; Linares-Vásquez, M.',
      venue: 'ACM TOSEM',
      year: '2024',
      bibkey: 'mastropaolo24tosem',
      affordance: 'Open paper'
    },
    'pub-icpc25': {
      kind: 'publication',
      title: 'Optimizing Datasets for Code Summarization: Is Code-Comment Coherence Enough?',
      shortLabel: 'Optimizing Datasets for Code Summarization',
      authors: 'Vitale, A.; Mastropaolo, A.; Oliveto, R.; Di Penta, M.; Scalabrino, S.',
      venue: 'ICPC',
      year: '2025',
      bibkey: 'vitale25icpc',
      affordance: 'Open paper'
    },
    'pub-forge': {
      kind: 'publication',
      title: 'Resource-Efficient & Effective Code Summarization',
      shortLabel: 'Resource-Efficient Code Summarization',
      authors: 'Afrin, S.; Call, J.; Nguyen, K.-N.; Chaparro, O.; Mastropaolo, A.',
      venue: 'FORGE',
      year: '2025',
      bibkey: 'afrin25forge',
      affordance: 'Open paper'
    },
    'pub-icpcera': {
      kind: 'publication',
      title: 'Toward Neurosymbolic Program Comprehension',
      shortLabel: 'Toward Neurosymbolic Program Comprehension',
      authors: 'Velasco, A.; Garryyeva, A.; Palacio, D. N.; Mastropaolo, A.; Poshyvanyk, D.',
      venue: 'ICPC ERA',
      year: '2025',
      bibkey: 'velasco25icpcera',
      affordance: 'Open paper'
    },
    'pub-icsme': {
      kind: 'publication',
      title: 'Is Quantization a Deal-breaker? Empirical Insights from Large Code Models',
      shortLabel: 'Is Quantization a Deal-breaker?',
      authors: 'Afrin, S.; Xu, B.; Mastropaolo, A.',
      venue: 'ICSME',
      year: '2025',
      bibkey: 'afrin25icsme',
      affordance: 'Open paper'
    },
    'pub-fseideas': {
      kind: 'publication',
      title: 'A Path Less Traveled: Reimagining Software Engineering Automation via a Neurosymbolic Paradigm',
      shortLabel: 'A Path Less Traveled',
      authors: 'Mastropaolo, A.; Poshyvanyk, D.',
      venue: 'FSE Ideas',
      year: '2025',
      bibkey: 'mastropaolo25fseideas',
      affordance: 'Open paper'
    },

    // People — director
    'p-am': {
      kind: 'people',
      role: 'Director · Principal Investigator',
      title: 'Antonio Mastropaolo',
      shortLabel: 'A. Mastropaolo',
      body: 'Assistant Professor, William & Mary CS. Ph.D., Università della Svizzera Italiana (2024). M.Sc. and B.Sc., University of Molise.',
      contact: 'amastropaolo@wm.edu',
      affordance: 'antoniomastropaolo.com'
    },

    // Ph.D. students
    'p-sa': {
      kind: 'people',
      role: 'Ph.D. student · joined Sep 2024',
      title: 'Saima Afrin',
      shortLabel: 'S. Afrin',
      body: 'Works on resource-efficient code summarization and quantization-aware evaluation of large code models.',
      affordance: 'View profile'
    },
    'p-ag': {
      kind: 'people',
      role: 'Ph.D. student · joined Jan 2025',
      title: 'Aya Garryyeva',
      shortLabel: 'A. Garryyeva',
      body: 'Works on neurosymbolic program comprehension and inspectable code reasoning.',
      affordance: 'View profile'
    },
    'p-jc': {
      kind: 'people',
      role: 'Ph.D. student · joined Jan 2025',
      title: 'Joseph Call',
      shortLabel: 'J. Call',
      body: 'Works on task-aware automation and resource-efficient summarization pipelines.',
      affordance: 'View profile'
    },
    'p-kn': {
      kind: 'people',
      role: 'Ph.D. student',
      title: 'Khai-Nguyen Nguyen',
      shortLabel: 'K. Nguyen',
      body: 'Works on summarization and task-aware code automation across repository signals.',
      affordance: 'View profile'
    },
    'p-alvi': {
      kind: 'people',
      role: 'Student',
      title: 'Alvi',
      shortLabel: 'Alvi',
      body: 'Lab student.',
      affordance: 'View profile'
    },
    'p-ben': {
      kind: 'people',
      role: 'Student',
      title: 'Ben',
      shortLabel: 'Ben',
      body: 'Lab student.',
      affordance: 'View profile'
    },
    'p-chris': {
      kind: 'people',
      role: 'Student',
      title: 'Chris',
      shortLabel: 'Chris',
      body: 'Lab student.',
      affordance: 'View profile'
    },

    // Collaborators
    'p-dp': {
      kind: 'people',
      role: 'Collaborator · W&M',
      title: 'Denys Poshyvanyk',
      shortLabel: 'D. Poshyvanyk',
      body: 'Frequent co-author on neurosymbolic and multi-agent SE research.',
      affordance: 'External profile'
    },
    'p-dnp': {
      kind: 'people',
      role: 'Collaborator',
      title: 'David Nader Palacio',
      shortLabel: 'D. N. Palacio',
      body: 'Frequent co-author on neurosymbolic program comprehension.',
      affordance: 'External profile'
    },
    'p-av': {
      kind: 'people',
      role: 'Collaborator',
      title: 'Alejandro Velasco',
      shortLabel: 'A. Velasco',
      body: 'Frequent co-author on neurosymbolic program comprehension.',
      affordance: 'External profile'
    },
    'p-oc': {
      kind: 'people',
      role: 'Collaborator',
      title: 'Oscar Chaparro',
      shortLabel: 'O. Chaparro',
      body: 'Frequent co-author on efficient code summarization.',
      affordance: 'External profile'
    },
    'p-bx': {
      kind: 'people',
      role: 'Collaborator',
      title: 'Bowen Xu',
      shortLabel: 'B. Xu',
      body: 'Frequent co-author on quantization for large code models.',
      affordance: 'External profile'
    },

    // Venues
    'v-tosem':   { kind: 'venue', title: 'ACM TOSEM',  shortLabel: 'TOSEM',    body: 'ACM Trans. Softw. Eng. and Methodology.', affordance: 'Venue site' },
    'v-icpc':    { kind: 'venue', title: 'ICPC',       shortLabel: 'ICPC',     body: 'IEEE/ACM Intl. Conf. on Program Comprehension.', affordance: 'Venue site' },
    'v-icpcera': { kind: 'venue', title: 'ICPC ERA',   shortLabel: 'ICPC ERA', body: 'ICPC Early Research Achievements track.', affordance: 'Venue site' },
    'v-forge':   { kind: 'venue', title: 'FORGE',      shortLabel: 'FORGE',    body: 'Intl. Conf. on AI Foundation Models and Software Engineering.', affordance: 'Venue site' },
    'v-icsme':   { kind: 'venue', title: 'ICSME',      shortLabel: 'ICSME',    body: 'IEEE Intl. Conf. on Software Maintenance and Evolution.', affordance: 'Venue site' },
    'v-fse':     { kind: 'venue', title: 'FSE Ideas',  shortLabel: 'FSE',      body: 'ACM Intl. Conf. on the Foundations of Software Engineering — Ideas, Visions, Reflections.', affordance: 'Venue site' }
  };

  // ---------- Build neighbor index from edges in the DOM ----------
  const svg = document.getElementById('graph');
  if (!svg) return;

  const neighborMap = new Map();
  function addNeighbor(a, b) {
    if (!neighborMap.has(a)) neighborMap.set(a, new Set());
    if (!neighborMap.has(b)) neighborMap.set(b, new Set());
    neighborMap.get(a).add(b);
    neighborMap.get(b).add(a);
  }

  const edges = svg.querySelectorAll('.edge');
  edges.forEach(e => {
    const a = e.getAttribute('data-a');
    const b = e.getAttribute('data-b');
    if (a && b) addNeighbor(a, b);
  });

  // edges indexed by id-pair
  function edgeKey(a, b) {
    return a < b ? a + '|' + b : b + '|' + a;
  }
  const edgeIndex = new Map();
  edges.forEach(e => {
    const a = e.getAttribute('data-a');
    const b = e.getAttribute('data-b');
    if (a && b) edgeIndex.set(edgeKey(a, b), e);
  });

  const nodes = svg.querySelectorAll('.node');
  const nodeIndex = new Map();
  nodes.forEach(n => nodeIndex.set(n.getAttribute('data-id'), n));

  // ---------- Highlight neighborhood ----------
  function clearHighlight() {
    svg.classList.remove('has-focus');
    nodes.forEach(n => n.classList.remove('focus', 'neighbor'));
    edges.forEach(e => e.classList.remove('active'));
  }

  function highlight(id) {
    if (!nodeIndex.has(id)) return;
    svg.classList.add('has-focus');
    nodes.forEach(n => n.classList.remove('focus', 'neighbor'));
    edges.forEach(e => e.classList.remove('active'));
    const focusEl = nodeIndex.get(id);
    focusEl.classList.add('focus');
    const neighbors = neighborMap.get(id) || new Set();
    neighbors.forEach(nb => {
      const el = nodeIndex.get(nb);
      if (el) el.classList.add('neighbor');
      const ek = edgeIndex.get(edgeKey(id, nb));
      if (ek) ek.classList.add('active');
    });
  }

  // ---------- Hover pub label ----------
  const pubHoverLabel = document.getElementById('pub-hover-label');
  function showPubLabel(node) {
    if (!pubHoverLabel) return;
    const id = node.getAttribute('data-id');
    const meta = NODES[id];
    if (!meta || meta.kind !== 'publication') {
      pubHoverLabel.classList.remove('show');
      return;
    }
    const cx = parseFloat(node.getAttribute('data-cx'));
    const cy = parseFloat(node.getAttribute('data-cy'));
    const labelDx = parseFloat(node.getAttribute('data-label-dx') || '0');
    const labelDy = parseFloat(node.getAttribute('data-label-dy') || '-18');
    pubHoverLabel.setAttribute('x', cx + labelDx);
    pubHoverLabel.setAttribute('y', cy + labelDy);
    pubHoverLabel.setAttribute('text-anchor', labelDx >= 0 ? 'start' : 'end');
    pubHoverLabel.textContent = (meta.shortLabel || meta.title) + ' — ' + meta.venue + ' ' + meta.year;
    pubHoverLabel.classList.add('show');
  }
  function hidePubLabel() {
    if (pubHoverLabel) pubHoverLabel.classList.remove('show');
  }

  // ---------- Drawer ----------
  const drawer = document.getElementById('drawer');
  const drawerKind = document.getElementById('drawer-kind');
  const drawerTitle = document.getElementById('drawer-title');
  const drawerBody = document.getElementById('drawer-body');
  const drawerMeta = document.getElementById('drawer-meta');
  const drawerAfford = document.getElementById('drawer-affordance');
  const drawerClose = document.getElementById('drawer-close');

  function renderDrawer(id) {
    const meta = NODES[id];
    if (!meta) return;
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');

    let kindLabel = meta.kind === 'avenue' ? 'Research avenue'
      : meta.kind === 'publication' ? 'Publication'
      : meta.kind === 'people' ? 'Person'
      : 'Venue';
    if (meta.tag) kindLabel += ' · ' + meta.tag;
    drawerKind.textContent = kindLabel;
    drawerTitle.textContent = meta.title;

    drawerBody.innerHTML = '';
    if (meta.body) {
      const p = document.createElement('p');
      p.textContent = meta.body;
      drawerBody.appendChild(p);
    }
    if (meta.authors) {
      const p = document.createElement('p');
      p.innerHTML = '<em>' + meta.authors + '</em>';
      drawerBody.appendChild(p);
    }

    drawerMeta.innerHTML = '';
    function addMeta(label, value) {
      if (!value) return;
      const dt = document.createElement('dt');
      dt.textContent = label;
      const dd = document.createElement('dd');
      dd.textContent = value;
      drawerMeta.appendChild(dt);
      drawerMeta.appendChild(dd);
    }
    if (meta.kind === 'publication') {
      addMeta('Venue', meta.venue);
      addMeta('Year', meta.year);
      addMeta('BibTeX key', meta.bibkey);
    } else if (meta.kind === 'people') {
      addMeta('Role', meta.role);
      addMeta('Contact', meta.contact);
    } else if (meta.kind === 'venue') {
      // nothing extra
    } else if (meta.kind === 'avenue') {
      // list connected publications
      const conns = (neighborMap.get(id) || new Set());
      const pubs = [...conns].filter(c => NODES[c] && NODES[c].kind === 'publication');
      if (pubs.length) {
        addMeta('Linked publications', pubs.map(p => NODES[p].shortLabel + ' (' + NODES[p].venue + ' ' + NODES[p].year + ')').join('  ·  '));
      }
    }

    drawerAfford.textContent = meta.affordance || 'View details';
  }

  function closeDrawer() {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    clearHighlight();
  }

  drawerClose.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeDrawer();
  });

  // ---------- Wire node events ----------
  nodes.forEach(n => {
    const id = n.getAttribute('data-id');

    n.addEventListener('mouseenter', () => {
      highlight(id);
      if (n.classList.contains('pub')) showPubLabel(n);
    });
    n.addEventListener('mouseleave', () => {
      if (!drawer.classList.contains('open')) clearHighlight();
      hidePubLabel();
    });
    n.addEventListener('click', (e) => {
      e.stopPropagation();
      highlight(id);
      renderDrawer(id);
    });
    n.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        highlight(id);
        renderDrawer(id);
      }
    });
  });

  // click outside graph closes
  document.addEventListener('click', (e) => {
    if (!drawer.contains(e.target) && !svg.contains(e.target)) {
      closeDrawer();
    }
  });

  // ---------- Default to director on load (subtle anchor for first-time viewers) ----------
  // We highlight but do NOT auto-open the drawer.
  setTimeout(() => {
    if (!drawer.classList.contains('open')) {
      highlight('p-am');
      setTimeout(() => {
        if (!drawer.classList.contains('open')) clearHighlight();
      }, 1600);
    }
  }, 600);
})();
