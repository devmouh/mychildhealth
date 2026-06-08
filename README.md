# 🏥 my child healthl Full-Stack Healthcare System (نظام my child health للرعاية الصحية)

<p align="center">
  <img src="backendcode/static/img/logo.png" alt="Zamil Logo" height="120">
</p>

---

## 🌍 Language Options / خيارات اللغة
- [English Documentation](#english-documentation)
- [التوثيق باللغة العربية](#التوثيق-باللغة-العربية)

---

# English Documentation

**my child health** is a premium, secure, and production-ready full-stack hospital and patient management workspace. It seamlessly integrates a cross-platform client app built with **Flutter** for patients and doctors, with a robust backend service engineered using **Django (REST API)** and backed by secure environment configurations.

## 🚀 Key Features
- 🩺 **Doctor Hub:** Manage appointments (approve/cancel), update profiles, write and publish educational medical blogs.
- 👤 **Patient Workspace:** Browse specialized doctors, schedule appointments, review consultation history, and read blogs.
- 🛡️ **Bilingual Localized System:** Seamless support for Arabic and English UI elements.
- ⚙️ **Admin Dashboard:** Full user management, platform notification distribution, and data audit logs.
- 🔒 **Security-First:** Token-based JWT Authentication, isolated environment variables, and production CORS protections.

---

## 🛠️ Stack & Architecture
- **Frontend App:** Flutter (State management: Provider, Client: Http).
- **Backend Service:** Python & Django REST Framework (DRF) with SimpleJWT.
- **Database:** SQLite (Default for development) & PostgreSQL support built-in for production.
- **Serving & Static Storage:** WhiteNoise for serving static files efficiently in production.
- **CI/CD & Containers:** Docker, Docker Compose, and GitHub Actions Pipelines.

---

## ⚡ Quick Start: One-Click Local Launch (Windows)

Running the entire full-stack project is now automated. No need to open multiple terminals or run complex commands manually!

1. **Launch the Stack:** Double-click the **`run_project.bat`** file in the root folder.
   - It will automatically create and set up your Python virtual environment (`venv`).
   - It will install all backend dependencies from `requirements.txt`.
   - It will execute database migrations (`migrate`) and prompt you to seed the database if it is a fresh install.
   - It will boot up the Django backend in a separate terminal window.
   - It will check your Flutter environment and ask you to launch the app on **Web (Chrome)** or a **Connected Device**.

---

## 📱 One-Click Android Compilation (APK Builder)

To build a secure, standalone APK for deployment or client testing:

1. **Compile the App:** Double-click the **`build_apk.bat`** file in the root folder.
2. **API Configuration:** It will prompt you to enter your deployed production backend API URL (e.g. `https://zamil-backend.onrender.com/api/`). Leave it empty to compile with the default development settings.
3. **Grab Your APK:** Once compiled, the script will automatically extract the release APK file and copy it to a new `/dist/` folder in your root directory as `dist/zamil-app-release.apk` for easy download and distribution.

---

## 🐳 Docker Deployment & Local Containers

To run the backend in a containerized environment (making it extremely easy to run across macOS, Linux, or Windows):

```bash
# Build and run the Django backend container
docker-compose up --build
```
The Django backend API will be available at `http://localhost:8000`.

---

## ☁️ Cloud Deployment & Production Hosting

### 1. Backend Deployment (Render / Heroku)
The project comes pre-configured with **Render Blueprint** configurations and a **Heroku Procfile**:
- **Render.com:** Simply connect your repository to Render and use the provided `render.yaml` template for instant deployment. It automatically handles PostgreSQL setup, static file collection, and boots Gunicorn.
- **Heroku:** Enable the python buildpack. The pre-configured `Procfile` instructs Heroku to run the production WSGI server automatically.

### 2. Frontend Web Deployment (Netlify / Vercel)
If you build the Flutter app for Web, you can deploy it statically to Netlify or Vercel:
```bash
# Build the web bundle
flutter build web --release --dart-define=API_BASE_URL=https://your-backend.com/api/
```
Deploy the static files generated inside `build/web` to Vercel/Netlify.

---

## 🔄 CI/CD & Automated Pipelines
A GitHub Actions workflow is pre-installed at `.github/workflows/deploy.yml`. When you commit to GitHub:
1. It automatically validates Django code formatting, imports, and system configuration.
2. It sets up Dart & Flutter to format, analyze, and build the client application, ensuring that code is always in a deployable state.

---
---

# التوثيق باللغة العربية

**my child health** هو نظام طبي متكامل لإدارة المستشفيات والرواد من الأطباء والمرضى، وهو جاهز تمامًا للإطلاق والإنتاج (Production-Ready). يدمج النظام بين واجهة أمامية متعددة المنصات (هواتف وويب) مطورة بإطار **Flutter**، وبنية خلفية قوية مبنية بـ **Django (REST API)** مع حماية معززة لكلمات المرور وعزل تام لإعدادات البيئة.

## 🚀 الميزات الأساسية
- 🩺 **لوحة الطبيب:** إدارة المواعيد وجدولتها (قبول/إلغاء)، تعديل الملف الشخصي، كتابة ونشر مقالات التثقيف الطبي.
- 👤 **لوحة المريض:** تصفح الأطباء حسب التخصصات، حجز مواعيد جديدة، مراجعة السجل والاستشارات الطبية السابقة، وقراءة مقالات الطبيب.
- 🛡️ **نظام معرب بالكامل:** توافق كامل مع الواجهات العربية والإنجليزية.
- ⚙️ **لوحة التحكم للمسؤولين (Admin):** إدارة شاملة للمستخدمين، وتوزيع الإشعارات العامة، ومتابعة سجلات التدقيق والنظام.
- 🔒 **حماية قصوى:** نظام توثيق مبني على رموز JWT المشفرة، حماية CORS، وعزل مفاتيح التشفير الحساسة.

---

## ⚡ التشغيل المحلي بضغطة زر واحدة (Windows)

لتسهيل تشغيل المشروع بدون أي خبرة تقنية سابقة أو كتابة أوامر معقدة:

1. **إقلاع النظام بالكامل:** انقر نقرًا مزدوجًا على ملف **`run_project.bat`** في المجلد الرئيسي للمشروع.
   - سيقوم السكريبت تلقائيًا بإنشاء البيئة الافتراضية للبايثون (`venv`).
   - سيثبت جميع المكتبات البرمجية المطلوبة من ملف `requirements.txt`.
   - سيقوم بتطبيق هجرات قاعدة البيانات ويسألك عما إذا كنت تريد تغذية قاعدة البيانات بالبيانات الافتراضية والنموذجية (Seed Data).
   - سيشغل الواجهة الخلفية لـ Django في نافذة منفصلة.
   - سيتحقق من وجود بيئة Flutter ويسألك عن مكان فتح التطبيق (المتصفح أو المحاكي).

---

## 📱 بناء وتصدير التطبيق بضغطة زر (APK Compiler)

إذا كنت ترغب في بناء تطبيق الأندرويد APK نهائي ومحمي لتثبيته أو رفعه على المتاجر:

1. **بناء التطبيق:** انقر نقرًا مزدوجًا على ملف **`build_apk.bat`** في المجلد الرئيسي.
2. **رابط الخادم:** سيطلب منك السكريبت إدخال عنوان خادم Django السحابي الخاص بك (مثال: `https://zamil-backend.onrender.com/api/`). إذا لم يكن لديك واحد بعد، اضغط ENTER لاستخدام إعدادات التطوير الافتراضية.
3. **تحميل الـ APK:** فور انتهاء البناء النظيف، سينقل السكريبت الملف النهائي إلى مجلد منظم جديد يسمى `/dist/` تحت اسم `dist/zamil-app-release.apk` لتنزيله أو مشاركته مباشرة وبسهولة.

---

## 🐳 حاويات دكر والتشغيل السحابي الموحد (Docker)

إذا كنت تستخدم نظام تشغيل آخر (مثل Linux أو macOS) أو ترغب بتشغيل المشروع في بيئة معزولة تمامًا:

```bash
# بناء وتشغيل الحاوية البرمجية الخاصة بالواجهة الخلفية
docker-compose up --build
```
سيكون خادم التطبيق متاحًا فورًا على العنوان الموحد `http://localhost:8000`.

---

## ☁️ النشر السحابي والإطلاق الفعلي

### 1. رفع الواجهة الخلفية (Render / Heroku)
المشروع مهيأ تمامًا للإطلاق المباشر بفضل ملفات التكوين المضمنة:
- **منصة Render.com:** يمكنك ربط مستودع الكود الخاص بك بالمنصة، وسيتولى ملف `render.yaml` بناء قاعدة البيانات وجلب الملفات الساكنة وتشغيل خادم الويب الإنتاجي `gunicorn` تلقائيًا.
- **منصة Heroku:** سيتعرف ملف `Procfile` المدمج في المجلد الخلفي على بيئة بايثون ويوجه الخادم للتشغيل الفوري.

### 2. رفع واجهة الويب (Netlify / Vercel)
في حال بناء واجهة التطبيق لتعمل كصفحة ويب، يمكنك رفعها مجانًا:
```bash
# بناء حزمة الويب للإنتاج
flutter build web --release --dart-define=API_BASE_URL=https://your-backend.com/api/
```
ارفع الملفات الموجودة في المجلد الناتج `build/web` إلى منصة Vercel أو Netlify.

---

## 🔄 التكامل المستمر والتطوير التلقائي (CI/CD)
تم إعداد ملف العمل الآلي التابع لـ GitHub Actions في المسار `.github/workflows/deploy.yml`. عند رفع الكود على GitHub:
1. يتم فحص الكود البرمجي لبايثون وDjango للتأكد من خلوه من الأخطاء المعمارية.
2. يتم تشغيل فاحص Flutter للتأكد من تنسيق الأكواد وجودتها لضمان نسخة خالية من المشاكل البرمجية دائمًا.
