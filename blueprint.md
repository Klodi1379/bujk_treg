# Blueprint i Zgjeruar për Platformën Bujqësore me Django

Ky blueprint përshkruan një plan të detajuar për ndërtimin e një platforme bujqësore duke përdorur Django me konfigurimet dhe funksionalitetet themelore, sipas kërkesave tuaja.

---

## Faza 1: Setup Bazë dhe Funksionalitete Themelore

### 1.1. Konfigurimi Fillestar i Projektit
- **Krijimi i projektit Django**: Përdorni komandën `django-admin startproject agricultural_platform` për të krijuar strukturën kryesore.
- **Baza e të dhënave**: Përdorim i konfigurimit default të Django (SQLite) për zhvillim fillestar.
- **Struktura e Projektit**:
  ```
  agricultural_platform/
  │
  ├── agricultural_platform/          # Direktoria kryesore e projektit (settings, urls, wsgi, asgi)
  │   ├── __init__.py
  │   ├── settings.py
  │   ├── urls.py
  │   ├── asgi.py
  │   └── wsgi.py
  │
  ├── farmer/                         # Aplikacioni për modulin e fermerëve
  │   ├── __init__.py
  │   ├── admin.py
  │   ├── models.py
  │   ├── views.py
  │   ├── forms.py
  │   ├── urls.py
  │   ├── templates/
  │   │   └── farmer/
  │   │       ├── register.html
  │   │       ├── profile.html
  │   │       ├── production_log.html
  │   │       └── dashboard.html
  │   └── static/
  │       └── farmer/
  │           ├── css/
  │           └── js/
  │
  ├── product/                        # Aplikacioni për modulin e produkteve
  │   ├── __init__.py
  │   ├── admin.py
  │   ├── models.py
  │   ├── views.py
  │   ├── forms.py
  │   ├── urls.py
  │   ├── templates/
  │   │   └── product/
  │   │       ├── catalog.html
  │   │       ├── detail.html
  │   │       ├── product_form.html
  │   │       └── manage_products.html
  │   └── static/
  │       └── product/
  │           ├── css/
  │           └── js/
  │
  ├── marketplace/                    # Aplikacioni për modulin e tregut
  │   ├── __init__.py
  │   ├── admin.py
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   └── templates/
  │       └── marketplace/
  │           ├── cart.html
  │           ├── order_confirmation.html
  │           └── order_history.html
  │
  ├── logistics/                      # Aplikacioni për modulin logjistik
  │   ├── __init__.py
  │   ├── admin.py
  │   ├── models.py
  │   ├── views.py
  │   ├── urls.py
  │   └── templates/
  │       └── logistics/
  │           └── tracking.html
  │
  ├── templates/                      # Template e përbashkëta
  │   ├── base.html
  │   ├── navbar.html
  │   └── footer.html
  │
  ├── static/                         # Asetet statike të përbashkëta
  │   ├── css/
  │   ├── js/
  │   └── images/
  │
  ├── media/                          # Skedarët e ngarkuar nga përdoruesit
  │
  ├── requirements.txt                # Varësitë e projektit
  │
  └── manage.py                       # Skripti i menaxhimit të Django
  ```

### 1.2. Menaxhimi i Përdoruesve dhe Autentikimi
- **Implementim i autentikimit**: Përdorim i sistemit të ndërtuar në Django (username/password).
- **Rollet e përdoruesit**: Ndryshimi i profilit për fermerë dhe blerës (p.sh., duke zgjeruar modelin e përdoruesit për fermerët).

### 1.3. Moduli i Fermerëve
- **Profilet e fermerëve**: Modelet për dhe forma për krijimin dhe përditësimin e profileve.
- **Menaxhimi i kulturave**: Modelet për kulturat, metodat e kultivimit, certifikimet dhe lidhjet me fermerët.
- **Regjistrimi i procesit të prodhimit**:
  - Krijimi i modeleve për `ProductionLog` për të gjurmuar aktivitetet e fermës.
- **Ngarkimi i dokumenteve dhe imazheve**: Përdorim i ruajtjes lokale për skedarët dhe imazhet.

### 1.4. Moduli i Produkteve
- **Produktet**: Modelet për produktet e fermerëve, përfshirë çmimet, sasinë, datat e vjeljes, dhe nëse janë organike/pesticide-free.
- **Katalogu Dixhital**: Implementimi i shikueshmërisë së produkteve, filtrave dhe kërkimit.
- **Imazhet e produkteve**: Menaxhimi i fotografive dhe lidhja me modelet për certifikimet.

### 1.5. Moduli i Tregut
- **Shporta dhe porositë**: Sistemi për shtimin e produkteve në shportë, përpunimi i porosive dhe përdorimi i metodës Cash on Delivery.
- **Paneli i porosive**: Forma dhe faqe për menaxhimin e porosive nga fermerët dhe blerësit.

### 1.6. Moduli Logjistik
- **Gjurmimi i dërgesave**: Modele dhe pamje për ndjekjen e statusit të porosive dhe lokacionin në kohë reale (thjesht për statusin, me plan për avancim).
- **Statusi i transportit**: Përditësime bazë për dërgesat, duke përdorur një sistem të thjeshtë për menaxhimin e tregtimeve.

---

## Faza 2: Integrimi i Ndërfaqes (UI/UX)

### 2.1. Template-et dhe Frontend Development
- **Dizajni Responsive**: Përdorimi i Bootstrap për të siguruar një interfaj modern dhe responsive.
- **Dashboard për fermerët**: Paneli ku fermerët mund të shohin produktet, hyrjet e prodhimit dhe porositë e fundit.
- **Katalogu i produkteve**: Pamje publike me filtrime, kërkim, dhe përshkrime të detajuara të produkteve.
- **Shporta e blerjeve**: Ndërtimi i sipërfaqes së porosive dhe pagesave (Cash on Delivery).

---

## Faza 3: Testimi dhe Dokumentimi

### 3.1. Testimi
- **Testime Njësie dhe Integrimi**: Sigurimi i funksionalitetit përmes testimeve automate.
- **Testimi i performancës**: Verifikimi i përputhshmërisë me kërkesat themelore të performancës.

### 3.2. Dokumentimi
- **Udhëzuesit për përdoruesit**: Dokumente të detajuara për mënyrën e përdorimit të platformës nga fermerët dhe blerësit.
- **Dokumentimi për zhvilluesit**: Përshkrime të modeleve, API-ve (nëse zhvillohet) dhe rrjedhave të biznesit.

---

## Faza 4: Përmirësime të Ardhshme

- **Integrimi i pagesave online**: Shtimi i metodave të pagesave si Visa, PayPal, etj.
- **Implementimi i Blockchain për gjurmueshmëri**: Për të përmirësuar transparencën dhe besimin.
- **Integrimi i IoT**: Për monitorim në kohë reale të produkteve gjatë transportit.
- **Migrimi në ruajtje cloud**: Përdorimi i AWS S3 ose alternativa për ruajtje të skedarëve.

---

## Përmbledhje
Ky blueprint ofron një udhëzues hap pas hapi për ndërtimin e një platforme bujqësore modulare me Django, duke përfshirë funksionalitetet kryesore për menaxhimin e fermerëve, produktet, tregun dhe logjistikën. Fillimisht, nisemi me konfigurimet themelore dhe funksionalitetin bazë ndërsa planifikojmë për përmirësime të ardhshme në bazë të nevojave dhe rritjes së përdoruesve.

---

Ky dokument shërben si një udhëzues për zbatimin e projektit dhe mund të përditësohet ndërkohë që zhvillohet projekti.
