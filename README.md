# RASPBERRY-QAM


# 🛰️ Système de Communication QAM via UDP entre deux Raspberry Pi

## 📌 Description

Ce projet implémente un système de communication numérique **semi-duplex** entre deux **Raspberry Pi 3 B**, utilisant le protocole **UDP** et la modulation **QAM** (Quadrature Amplitude Modulation) pour la transmission de **messages texte, images et fichiers audio**. L’architecture logicielle est modulaire, développée en Python, avec une interface graphique simple pour l’utilisateur.

---

## 🎯 Objectifs

- Créer un **modulateur/démodulateur QAM** (4, 16, 64 ou 256-QAM)
- Implémenter une communication **UDP** bidirectionnelle entre deux Raspberry Pi
- Supporter l’échange de **texte, images et audio**
- Concevoir une **interface graphique** avec Tkinter
- Gérer l’**authentification**, la **synchronisation** et la **structuration des paquets**

---

## 🧱 Architecture du Projet

```
📦 raspberry_qam_project/
├── chat_ui.py          # Interface graphique (Tkinter)
├── chat_backend.py     # Moteur réseau UDP et logique de transmission
├── qam_utils.py        # Algorithmes de modulation et démodulation QAM
├── audio_utils.py      # Traitement et lecture des fichiers audio
├── config.py           # Paramètres réseau, starter bit, mot de passe
```

---

## ⚙️ Fonctionnement Technique

### 🔁 Communication

- Protocole : **UDP (socket)**
- Type : **semi-duplex**
- Paquets : envoyés par segments avec temporisation (`SEND_DELAY`)
- Synchronisation : ajout d’un **STARTER_BIT** unique en début de message

### ⚡ Choix de l'UDP

Le protocole **UDP** a été choisi pour sa simplicité et sa faible latence. Cependant, il **ne garantit pas la livraison des paquets**. Pour pallier cela :

- Les messages sont envoyés **avec un bit de synchronisation personnalisé** (STARTER_BIT)
- Un **délai** est introduit entre les envois (`SEND_DELAY = 0.01`)
- Le format `<END>` marque la fin de chaque message
- L’audio est divisé en **chunks numérotés**

---

## 📁 Détail des fichiers Python

### `chat_backend.py`
- Gère l'envoi/réception via **UDP**
- Types de messages : `TEXT`, `IMAGE`, `AUDIO_CHUNK`, `STATUS`
- Utilise :
  - `qam_utils.py` pour la modulation QAM
  - `audio_utils.py` pour le son
  - `config.py` pour l’IP, le port et le `STARTER_BIT`

### `chat_ui.py`
- Interface graphique avec **Tkinter**
- Composants :
  - Champ texte + boutons d’envoi (texte, image, audio)
  - Menu déroulant pour le **choix du schéma QAM**
  - Indicateur d’état du correspondant

### `qam_utils.py`
- Gère :
  - `qam_modulate(bits, M)` : bits → symboles complexes IQ
  - `qam_demodulate(symbols, M)` : symboles IQ → bits
- Compatible avec : **4, 16, 64, 256-QAM**

### `audio_utils.py`
- Gère les fichiers `.wav`
- Fonctions :
  - `load_wav_file()` / `save_wav_file()`
  - `play_audio()` (avec `sounddevice`)
  - `audio_to_bits()` / `bits_to_audio()`

### `config.py`
- IP du destinataire : `RECEIVER_IP`
- Port UDP : `PORT = 5005`
- Mot de passe : `AUTH_PASSWORD`
- `STARTER_BIT = np.array([1, 0, 1, 0, 1, 0, 1, 0])`

---

## 🖼️ Interface Utilisateur

Interface simple mais fonctionnelle :
- Zone de chat
- Envoi de :
  - ✅ Message texte
  - 🖼️ Fichier image
  - 🔊 Fichier audio
- Sélecteur du schéma de modulation (4/16/64/256-QAM)
- Statut de l’autre Raspberry Pi (en ligne / hors ligne)

---

## 🔍 Points clés & défis techniques

| Problème rencontré                  | Solution mise en place                                         |
|------------------------------------|----------------------------------------------------------------|
| Perte de paquets UDP (audio)       | Réduction des chunks + temporisation entre envois              |
| Synchronisation instable           | Introduction de `STARTER_BIT` et de séquences `<END>`          |
| Audio fragmenté ou haché           | Réindexation des chunks + buffer audio pour réassemblage       |
| Interface figée en cas d’erreur    | Ajout de messages d’erreur dans `chat_window` pour débogage    |

---

## 🚀 Lancer le Projet

1. Adapter l’IP de la Raspberry Pi cible dans `config.py`
2. Lancer `chat_ui.py` sur les deux Raspberry Pi :
```bash
python3 chat_ui.py
```
3. Choisir un schéma QAM (ex: 16-QAM)
4. Échanger des messages, images ou fichiers audio

---

## 👨‍💻 Auteurs

Projet développé par :

- Hammouchi Louay
- Tardaoui Sohaib
- El Maalmi Mohammed
- Mohamed Iyad Lahrech
- Mohamed Ali Belabdia
- **Megder Mohamed Al Amine**

Encadré par : **Pr. Naoufal RAISSOUNI**

---

## 📚 Technologies utilisées

- **Python 3.10+**
- `socket`, `tkinter`, `numpy`, `sounddevice`, `scipy`
- **UDP**, **QAM**, **Threading**, **Tkinter GUI**

---

## 📦 Possibilités futures

- Ajout d’une couche de **sécurité/chiffrement**
- Passage à **TCP** avec ARQ pour fiabilité
- Compression des fichiers transmis
- Envoi en **streaming audio/vidéo en temps réel**
