# Configuration Claude Code pour ATLAS

Ce dossier contient les instructions, six skills personnalisés et trois sous-agents de revue pour le projet ATLAS.

## Installation

Copie le contenu de ce dossier à la racine du dépôt ATLAS en conservant la structure :

```text
atlas/
├── CLAUDE.md
└── .claude/
    ├── agents/
    │   ├── code-reviewer.md
    │   ├── data-auditor.md
    │   └── econometrics-reviewer.md
    └── skills/
        ├── data-source-audit/SKILL.md
        ├── geospatial-analysis/SKILL.md
        ├── python-data-pipeline/SKILL.md
        ├── research-design/SKILL.md
        ├── r-econometrics/SKILL.md
        └── scientific-review/SKILL.md
```

Depuis le dossier du projet, les fichiers peuvent être copiés avec :

```bash
cp -r /chemin/vers/atlas-claude-config/CLAUDE.md .
cp -r /chemin/vers/atlas-claude-config/.claude .
```

Remplace `/chemin/vers/atlas-claude-config` par le chemin réel de l'archive extraite. Vérifie avant de copier si le dépôt contient déjà un `CLAUDE.md` ou un dossier `.claude`, afin de ne pas écraser une configuration existante.

## Utilisation

- Les règles générales sont chargées depuis `CLAUDE.md`.
- Les skills sont stockés dans `.claude/skills/<nom-du-skill>/SKILL.md`.
- Les sous-agents sont stockés dans `.claude/agents/`.
- Dans Claude Code, vérifie la disponibilité des skills et agents avec les commandes d'aide disponibles dans la version installée. Les noms de fichiers sont les identifiants attendus.

## Bonnes pratiques

- Commence par l'audit de faisabilité des sources et le design de recherche.
- N'active pas toutes les procédures à chaque tâche ; utilise celle qui correspond au travail demandé.
- Lis et ajuste ces instructions après la phase 0, quand le périmètre et les données seront confirmés.
- Ces fichiers guident Claude, mais ne garantissent pas la justesse des résultats. Les tests et la revue scientifique restent nécessaires.

## Limite des agents de revue (vérifiée pour Claude Code 2.1.296)

Les trois agents ont `tools: Read, Grep, Glob, Bash`. Write, Edit et NotebookEdit sont donc réellement indisponibles pour eux. **Bash n'est pas en lecture seule** : une commande shell peut écrire ou supprimer des fichiers. L'absence de modification repose sur la consigne de l'agent et sur le mode de permission de la session, pas sur une restriction technique.

Options examinées et non retenues :
- Retirer Bash : empêcherait de lancer pytest, Rscript ou de lire des fichiers Parquet.
- `disallowedTools: Bash(...)` : un motif retire Bash entièrement, il ne filtre pas les commandes.
- `permissionMode: plan` dans l'agent : ignoré lorsque la session principale est en mode auto, acceptEdits ou bypassPermissions.
- Hook `PreToolUse` avec liste noire de commandes : contournable (`python -c`, redirections, `sed -i`, etc.), donc faux sentiment de sécurité.

Pour un contrôle effectif, lance la session en mode par défaut (chaque commande Bash est soumise à validation) ou ajoute des règles `permissions.deny` dans `.claude/settings.json`.
