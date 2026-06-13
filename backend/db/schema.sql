-- Table pour historiser les imports de fichiers
CREATE TABLE IF NOT EXISTS imports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_fichier TEXT NOT NULL,
    date_import DATETIME DEFAULT CURRENT_TIMESTAMP,
    lignes_traitees INTEGER NOT NULL,
    statut TEXT NOT NULL -- Exemple : 'SUCCÈS', 'ÉCHEC'
);

-- Table des classes
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE
);

-- Table des étudiants
CREATE TABLE IF NOT EXISTS etudiants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricule TEXT UNIQUE NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE,
    classe_id INTEGER,
    FOREIGN KEY (classe_id) REFERENCES classes (id) ON DELETE SET NULL
);

-- Table des modules (matières)
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    coefficient INTEGER DEFAULT 1
);

-- Table des notes
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    valeur REAL NOT NULL CHECK(valeur >= 0 AND valeur <= 20),
    date_evaluation DATE,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants (id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES modules (id) ON DELETE CASCADE
);

-- Table des absences
CREATE TABLE IF NOT EXISTS absences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER NOT NULL,
    date_absence DATE NOT NULL,
    justifiee BOOLEAN DEFAULT 0,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants (id) ON DELETE CASCADE
);

-- Table des alertes pédagogiques
CREATE TABLE IF NOT EXISTS alertes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    etudiant_id INTEGER NOT NULL,
    type_alerte TEXT NOT NULL, -- Exemple: 'RISQUE_ECHEC', 'ABSENTEISME'
    message TEXT NOT NULL,
    date_alerte DATETIME DEFAULT CURRENT_TIMESTAMP,
    est_resolue BOOLEAN DEFAULT 0,
    FOREIGN KEY (etudiant_id) REFERENCES etudiants (id) ON DELETE CASCADE
);
