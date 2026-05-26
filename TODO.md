# Advanced Django Ecommerce — Daily Progress Tracker

**Stack:** Django (MVT, no API) · PostgreSQL · Redis · Celery · Bootstrap 5 · HTMX · Stripe/Razorpay · AWS S3 · Docker
**Start:** 2026-05-25 · **Deadline:** ~2026-06-24 (30 days)

---

## 📍 CURRENT STATUS (update this daily)

- **Today's Date:** 2026-05-25
- **Currently working on:** Day 1 — Project Setup
- **Last completed:** _(none yet)_
- **Next up:** Day 1 — Project Setup
- **Carry-over tasks (incomplete from previous days):** _(none yet)_
- **Overall progress:** 0 / 30 days

> 📝 **How to use this tracker:**
> - Tick `[x]` each sub-task as you finish it.
> - If a day's sub-tasks aren't all done, **copy unfinished items to the next day's "Carry-over" section** and update "Currently working on" above.
> - Mark a Day's heading with ✅ only when ALL its sub-tasks are checked.
> - Update "Today's Date" + "Currently working on" + "Last completed" every day.

---

## 🗺️ Module Completion Tracker

- [ ] 1. Auth & User Management
- [ ] 2. Product Catalog
- [ ] 3. Search & Filter
- [ ] 4. Cart & Wishlist
- [ ] 5. Checkout & Orders
- [ ] 6. Payments
- [ ] 7. Vendor / Multi-seller
- [ ] 8. Coupons & Promotions
- [ ] 9. Notifications
- [ ] 10. Admin Dashboard
- [ ] 11. Performance & Production
- [ ] 12. Security
- [ ] 13. Testing & Quality

---

## 🗄️ Database Schema Completion

- [ ] **Users:** User · UserProfile · Address
- [ ] **Catalog:** Category (MPTT) · Brand · Product · ProductImage · Attribute · AttributeValue · ProductVariant · ProductVariant_Attribute · ProductReview · ReviewImage · Tag · Product_Tag
- [ ] **Cart:** Cart · CartItem · Wishlist · WishlistItem
- [ ] **Orders:** Order · OrderItem · OrderStatusHistory · Shipment · ReturnRequest
- [ ] **Payments:** Payment · Refund
- [ ] **Promotions:** Coupon · CouponUsage
- [ ] **Vendors:** Vendor · Payout
- [ ] **Misc:** Notification · Banner · ShippingZone · Tax

---

# 📅 WEEK 1 — Foundation, Auth & Catalog

## Day 1 — Project Setup & Base Template
**Status:** 🔲 Not started | **Date done:** _____

- [x] Create virtualenv + install Django, psycopg2, python-decouple
- [x] `django-admin startproject core .`
- [x] Split settings (`settings/base.py`, `dev.py`, `prod.py`)
- [x] `.env` file + `.gitignore`
- [x] PostgreSQL database created + connected
- [x] Initial migration runs successfully
- [ ] Git repo init + first commit
- [ ] Base template (`templates/base.html`) with Bootstrap 5 CDN
- [ ] Partials: `_navbar.html`, `_footer.html`, `_messages.html`, `_pagination.html`
- [ ] `base_auth.html`, `base_dashboard.html` layouts
- [ ] Static folder structure (`static/css/`, `static/js/`, `static/images/`)
- [ ] Global CSS file with color variables
- [ ] Home page view + URL working

**Carry-over from previous day:** _(none)_
**Notes:** _____

---

## Day 2 — Custom User Model & Auth Basics
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Create `accounts` app
- [ ] Custom User Model (AbstractBaseUser, UUID PK, email login)
- [ ] UserManager with `create_user` + `create_superuser`
- [ ] `AUTH_USER_MODEL` in settings
- [ ] Registration form + view + template
- [ ] Login form + view + template
- [ ] Logout view
- [ ] Email verification token (generate + send + verify URL)
- [ ] Email backend setup (console for dev)

**Carry-over from previous day:** _____
**Notes:** _____

---

## Day 3 — Password Reset, Social Auth, Profile, Address
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Password reset flow (request → email → reset form → done)
- [ ] django-allauth install + config (Google + Facebook)
- [ ] UserProfile model + OneToOne signal
- [ ] Profile view + edit form + template
- [ ] Address model (multi-address, is_default)
- [ ] Address list / add / edit / delete views + templates

**Carry-over from previous day:** _____
**Notes:** _____

---

## Day 4 — Category (MPTT) & Brand
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Create `catalog` app
- [ ] Install django-mptt
- [ ] Category model (MPTT, slug, image, parent)
- [ ] Brand model
- [ ] Customize Django admin for Category (tree view) + Brand
- [ ] Seed sample categories + brands (management command or fixtures)
- [ ] Category list page + nested menu in navbar

**Carry-over from previous day:** _____
**Notes:** _____

---

## Day 5 — Product Model & Listing/Detail Pages
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Product model (UUID, FK category/brand, price, slug, SEO fields)
- [ ] ProductImage model (primary, order)
- [ ] Django admin inline for ProductImage
- [ ] Product list view (`/products/`) + template (Bootstrap card grid)
- [ ] Product detail view (`/products/<slug>/`) + template
- [ ] Image gallery on detail page
- [ ] Seed sample products

**Carry-over from previous day:** _____
**Notes:** _____

---

## Day 6 — Attributes & Variants
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Attribute model (Color, Size, etc.)
- [ ] AttributeValue model
- [ ] ProductVariant model (sku, price, stock)
- [ ] ProductVariant_Attribute M2M through model
- [ ] Variant selector UI on product detail page (HTMX optional)
- [ ] Price + stock updates based on selected variant
- [ ] Auto SKU generation

**Carry-over from previous day:** _____
**Notes:** _____

---

## Day 7 — Reviews, Tags, Related Products + Week 1 Buffer
**Status:** 🔲 Not started | **Date done:** _____

- [ ] ProductReview model + ReviewImage
- [ ] Review form + view (only verified buyers if logged in)
- [ ] Display reviews + average rating on product detail
- [ ] Tag model + Product_Tag M2M
- [ ] Related products query (same category/brand/tags)
- [ ] Week 1 buffer: fix bugs, polish, push to GitHub

**Carry-over from previous day:** _____
**Notes:** _____

---

# 📅 WEEK 2 — Search, Cart, Wishlist, Checkout

## Day 8 — Search & Filters
**Status:** 🔲 Not started | **Date done:** _____

- [ ] PostgreSQL full-text search (`SearchVector`, `SearchQuery`)
- [ ] Search results page
- [ ] Filter form (price range, brand, attributes, rating)
- [ ] Sort dropdown (price asc/desc, newest, popular, rating)
- [ ] Pagination

**Carry-over:** _____ | **Notes:** _____

---

## Day 9 — HTMX Autocomplete & AJAX Filters
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Add HTMX to base template
- [ ] Search autocomplete dropdown
- [ ] Filter updates without page reload
- [ ] Loading spinner / skeleton states

**Carry-over:** _____ | **Notes:** _____

---

## Day 10 — Cart (Session + DB) & Merge
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Cart + CartItem models
- [ ] Cart context processor (cart count in navbar)
- [ ] Add to cart (works for guest via session + user via DB)
- [ ] Update quantity / remove item
- [ ] Merge guest cart → user cart on login (signal)

**Carry-over:** _____ | **Notes:** _____

---

## Day 11 — Wishlist, Save-for-Later, Cart UI Polish
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Wishlist + WishlistItem models
- [ ] Add/remove wishlist
- [ ] Save-for-later toggle on cart items
- [ ] Cart page polish (Bootstrap, responsive)

**Carry-over:** _____ | **Notes:** _____

---

## Day 12 — Checkout Step 1: Address
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Checkout flow setup (session-based state)
- [ ] Address selection page (use saved or add new)
- [ ] Validate address before proceeding

**Carry-over:** _____ | **Notes:** _____

---

## Day 13 — Checkout Step 2: Shipping, Tax, Coupon
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Shipping zones + rate calculation
- [ ] Tax calculation (GST/VAT)
- [ ] Coupon application form (validate, apply discount)
- [ ] Order summary with totals

**Carry-over:** _____ | **Notes:** _____

---

## Day 14 — Order Placement (COD) + Email
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Order + OrderItem models
- [ ] Order placement view (creates Order, snapshots address/prices)
- [ ] Order confirmation page
- [ ] Celery + Redis setup
- [ ] Order confirmation email task

**Carry-over:** _____ | **Notes:** _____

---

# 📅 WEEK 3 — Payments, Orders, Vendor, Admin

## Day 15 — Stripe/Razorpay Integration
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Payment model
- [ ] Stripe (or Razorpay) checkout session (server-rendered)
- [ ] Success / cancel pages
- [ ] Update order status on payment

**Carry-over:** _____ | **Notes:** _____

---

## Day 16 — Webhooks & Refunds
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Webhook endpoint + signature verification
- [ ] Sync payment status via webhook
- [ ] Refund model + initiate refund flow

**Carry-over:** _____ | **Notes:** _____

---

## Day 17 — Order List, Detail, Tracking, Cancel/Return
**Status:** 🔲 Not started | **Date done:** _____

- [ ] User order list page
- [ ] Order detail page with status timeline
- [ ] OrderStatusHistory tracking
- [ ] Cancel order flow
- [ ] ReturnRequest model + request form

**Carry-over:** _____ | **Notes:** _____

---

## Day 18 — Invoice PDF
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Install WeasyPrint
- [ ] Invoice HTML template
- [ ] Generate PDF view (download)
- [ ] Email invoice as attachment

**Carry-over:** _____ | **Notes:** _____

---

## Day 19 — Coupons & Banners Admin
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Coupon model + CouponUsage
- [ ] Admin CRUD for coupons
- [ ] Banner model + admin
- [ ] Homepage banner display

**Carry-over:** _____ | **Notes:** _____

---

## Day 20 — Vendor Module
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Vendor model + approval workflow
- [ ] Vendor registration form
- [ ] Vendor dashboard layout
- [ ] Vendor product CRUD (own products only)
- [ ] Vendor order list (orders containing their products)

**Carry-over:** _____ | **Notes:** _____

---

## Day 21 — Custom Admin Dashboard
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Admin dashboard layout (sidebar)
- [ ] Sales analytics (Chart.js — daily/weekly/monthly)
- [ ] Top products / top customers widgets
- [ ] Low stock alerts list
- [ ] Order management (status updates)

**Carry-over:** _____ | **Notes:** _____

---

# 📅 WEEK 4 — Performance, Security, Testing, Deployment

## Day 22 — Redis Cache & Query Optimization
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Redis as cache backend
- [ ] Cache product list / category pages
- [ ] Use `select_related` / `prefetch_related` in heavy views
- [ ] Django Debug Toolbar audit

**Carry-over:** _____ | **Notes:** _____

---

## Day 23 — Celery Async Tasks
**Status:** 🔲 Not started | **Date done:** _____

- [ ] All emails via Celery
- [ ] Image thumbnail generation task (Pillow)
- [ ] Order reminder / abandoned cart task (Celery Beat)

**Carry-over:** _____ | **Notes:** _____

---

## Day 24 — Security Hardening
**Status:** 🔲 Not started | **Date done:** _____

- [ ] django-axes (brute-force lockout)
- [ ] django-ratelimit on login/register
- [ ] reCAPTCHA on signup/login
- [ ] CSP headers (django-csp)
- [ ] SECURE_* settings for prod

**Carry-over:** _____ | **Notes:** _____

---

## Day 25 — AWS S3 + Static Files
**Status:** 🔲 Not started | **Date done:** _____

- [ ] django-storages + boto3
- [ ] S3 bucket setup, IAM user
- [ ] Media uploads → S3
- [ ] WhiteNoise for static
- [ ] Image optimization (Pillow, max dimensions)

**Carry-over:** _____ | **Notes:** _____

---

## Day 26 — Testing
**Status:** 🔲 Not started | **Date done:** _____

- [ ] pytest + pytest-django setup
- [ ] factory_boy + faker
- [ ] Unit tests: models, forms
- [ ] Integration tests: cart, checkout, order flow
- [ ] Coverage report > 80%

**Carry-over:** _____ | **Notes:** _____

---

## Day 27 — Dockerize
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Dockerfile (multi-stage)
- [ ] docker-compose.yml (web, db, redis, celery, nginx)
- [ ] .dockerignore
- [ ] Local docker-compose up working

**Carry-over:** _____ | **Notes:** _____

---

## Day 28 — CI/CD + Sentry
**Status:** 🔲 Not started | **Date done:** _____

- [ ] GitHub Actions workflow (lint, test)
- [ ] Deploy step (Railway / DO / EC2)
- [ ] Sentry integration (django + celery)
- [ ] Pre-commit hooks (black, isort, flake8)

**Carry-over:** _____ | **Notes:** _____

---

## Day 29 — Production Deploy
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Provision server / Railway project
- [ ] Domain + DNS
- [ ] SSL (Certbot / Cloudflare)
- [ ] Nginx + Gunicorn config
- [ ] Smoke test full flow on prod

**Carry-over:** _____ | **Notes:** _____

---

## Day 30 — Final QA, Docs, Demo
**Status:** 🔲 Not started | **Date done:** _____

- [ ] Full end-to-end QA (register → buy → refund)
- [ ] Fix bugs found
- [ ] Write README (features, setup, deploy, screenshots)
- [ ] Record demo video / GIF
- [ ] Tag v1.0.0 release

**Carry-over:** _____ | **Notes:** _____

---

## 🚧 Backlog / Postponed Tasks

_(Move any task here that's deferred to "later" — keeps daily sections clean)_

- _____

---

## 🐛 Bug Log

_(Track bugs found during the build)_

| Date | Bug | Fix | Status |
|------|-----|-----|--------|
| | | | |

---

## 💡 Concepts Learned (Personal Knowledge Log)

_(Quick notes as you learn — helps for the DRF+Vue rebuild later)_

- _____
