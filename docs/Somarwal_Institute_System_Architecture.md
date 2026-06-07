# System Architecture Document (SAD)
## Somarwal Computer & Tech Institute, Ajmer

---

## 1. Frontend Architecture
The frontend is built as a Single Page Application (SPA) or Server-Side Rendered (SSR) application to ensure fast load times and SEO optimization.
* **Core Framework:** React.js or Next.js.
* **Styling:** Tailwind CSS for a utility-first, highly responsive design.
* **State Management:** Redux Toolkit or React Context API for managing global states like user authentication, cart/course selection, and UI toggles.
* **Routing:** React Router (for React SPA) or Next.js File-Based Routing.
* **Component Structure:** Atomic design principles (Atoms: Buttons, Inputs; Molecules: Cards, Forms; Organisms: Headers, Grids; Templates/Pages).

## 2. Backend Architecture
The backend serves as a RESTful API provider using a layered/MVC (Model-View-Controller) architecture.
* **Core Framework:** Node.js with Express.js (or Django/Laravel as alternatives).
* **Architecture Pattern:**
  * **Controllers:** Handle incoming HTTP requests and map them to business logic.
  * **Services:** Contain the core business logic (e.g., calculating fees, formatting PDFs).
  * **Data Access Layer / Models:** Interface with the database using an ORM (e.g., Prisma, Sequelize, or Mongoose if NoSQL was used, but Relational is preferred here).

## 3. Database Architecture
A relational database ensures data integrity across complex relationships (e.g., a student belongs to multiple courses, has multiple payments).
* **Database Engine:** MySQL or PostgreSQL.
* **Core Entities & Relationships:**
  * **Users/Admins:** Credentials and role definitions.
  * **Students:** Personal details, contact info.
  * **Courses:** Name, duration, fees, modules (1-to-Many with Syllabi).
  * **Admissions/Enrollments:** Junction table linking Students and Courses, storing unique Registration IDs.
  * **Payments:** Linked to Enrollments, stores transaction IDs and status.
  * **Certificates:** Linked to Enrollments, stores unique Certificate IDs and validity.

## 4. Storage Architecture
Separation of application code and static media/documents.
* **Database:** Stores structured text data and file URLs.
* **Cloud Storage:** Amazon S3 or Cloudinary.
  * Stores heavy assets: Gallery photos, Director's images, Student avatars.
  * Stores generated PDFs: Fee receipts and generated Certificates.
* **Local Temp Storage:** Ephemeral backend storage used temporarily during PDF generation before syncing to Cloud Storage.

## 5. API Communication
* **Protocol:** HTTPS RESTful APIs.
* **Format:** JSON payloads.
* **Client Interface:** Axios or Native Fetch API.
* **Middleware:** * `cors`: Cross-Origin Resource Sharing configuration.
  * `helmet`: HTTP header security.
  * `express-validator`: Payload validation before processing logic.

## 6. Authentication Flow
Securing the Admin Dashboard and protected endpoints.
1. Admin submits username/password.
2. Backend queries DB and verifies password hash (e.g., via `bcrypt`).
3. If valid, backend generates a JSON Web Token (JWT) containing the user ID and Role.
4. Token is returned to the client and stored (preferably in an `HttpOnly` cookie or secure LocalStorage).
5. For subsequent requests, the frontend attaches the JWT in the `Authorization: Bearer <token>` header.
6. Backend middleware verifies the JWT signature before granting route access.

## 7. Session Management
* **Stateless Sessions:** Managed entirely via JWT to reduce database load.
* **Token Expiration:** Short-lived Access Tokens (e.g., 1-2 hours) and longer-lived Refresh Tokens (e.g., 7 days) to maintain persistent login state securely.
* **Role-Based Access Control (RBAC):** Token payload dictates whether a user can perform Write/Delete operations or is restricted to Read-Only.

## 8. Payment Flow
Integration with a Payment Gateway (e.g., Razorpay, Stripe, or PhonePe).
1. Student fills admission form and clicks "Pay Now".
2. Frontend requests an Order ID from the Backend.
3. Backend creates an Order with the Payment Gateway and returns the Order ID.
4. Frontend initializes the Payment Gateway widget.
5. User completes payment via UPI, Card, or NetBanking.
6. Payment Gateway triggers a Server-to-Server **Webhook** to the Backend to confirm success.
7. Backend updates DB, marks payment as "Success", generates the PDF Receipt, and triggers emails/WhatsApp.

## 9. WhatsApp Integration Flow
Automated notifications using WhatsApp Business API (Meta Graph API or Twilio).
1. Event Triggered: e.g., Admission is marked 'Confirmed' in DB.
2. Backend Service constructs a pre-approved WhatsApp Template Message containing variables (Student Name, Course, Reg ID).
3. Backend POST request is sent to the WhatsApp API endpoint with the destination phone number.
4. WhatsApp API responds with a Message ID or Error.
5. Backend logs the delivery status in the database.

## 10. Certificate Verification Flow
Secure, read-only public access to verify credentials.
1. User (Employer/Student) navigates to `/verify-certificate` on the frontend.
2. User enters `Certificate ID` or `Registration Number` and submits.
3. Frontend makes a GET request to `/api/certificates/verify?id=XXX`.
4. Backend runs a sanitized, exact-match query against the database (preventing wildcard scraping).
5. If found AND status is "Active", backend returns student name, course, and date.
6. Frontend displays a "Verified - Authentic" digital badge with the details.
