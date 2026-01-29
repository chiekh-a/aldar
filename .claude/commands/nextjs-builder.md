---
description: Complete NextJS 15 Application Setup
---
You are an expert NextJS developer tasked with scaffolding a production-ready NextJS application with modern best practices, authentication, analytics, and email capabilities.

## Execution Steps

### 1. Initialize NextJS Application
- Create a new NextJS 15 app with TypeScript, Tailwind CSS, and App Router, using CLI flags
- Use NextJS 15
- Configure `next.config.js` for optimal performance

### 2. Project Structure Setup
Create the following organized folder structure:
```
nextjs-app/
├── app/
│   ├── api/
│   │   ├── webhooks/
│   │   │   ├── stripe/route.ts
│   │   │   └── clerk/route.ts
│   │   └── send-email/route.ts
│   │
│   ├── [locale]/
│   │   ├── auth/
│   │   │   ├── sign-in/page.tsx
│   │   │   ├── sign-up/page.tsx
│   │   │   └── layout.tsx
│   │   │
│   │   ├── dashboard/
│   │   │   ├── _components/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   │
│   │   ├── preview/page.tsx
│   │   │
│   │   ├── (marketing)/
│   │   │   ├── _components/
│   │   │   ├── about/page.tsx
│   │   │   ├── pricing/page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   │
│   │   ├── layout.tsx
│   │   └── not-found.tsx
│   │
│   ├── layout.tsx
│   ├── global-error.tsx
│   ├── sitemap.ts
│   └── robots.ts
│
├── components/
│   ├── ui/
│   ├── layouts/
│   └── common/
│
├── hooks/
│
├── lib/
│   ├── db/
│   │   ├── schema/
│   │   ├── migrations/
│   │   └── index.ts
│   ├── stripe/
│   ├── i18n/
│   ├── email/
│   └── utils.ts
│
├── providers/
│   ├── clerk-provider.tsx
│   ├── posthog-provider.tsx
│   └── index.tsx
│
├── types/
│
├── config/
│   ├── site.ts
│   └── nav.ts
│
├── middleware.ts
│
├── public/
│   └── images/
│
├── next.config.ts
├── tailwind.config.ts
├── drizzle.config.ts
├── .env.local
└── .env.example
```
- **No duplicate routes**: If you create `[locale]/dashboard`, do NOT also have `/dashboard`
- **Route groups need content**: Every route group `(name)` must have page.tsx files inside
- **Clean as you go**: When moving shadcn-generated files, delete empty source folders immediately
- **Verify structure**: After each major step, use `ls` to verify folders contain expected files
- **Locale-first routing**: ALL user-facing routes go under `[locale]/`, NO exceptions

### 3. Environment Variables Setup
Create `.env.example` with:
```env
# Database
DATABASE_URL=

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/auth/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/auth/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
CLERK_WEBHOOK_SECRET=

# Stripe
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# Resend
RESEND_API_KEY=
RESEND_FROM_EMAIL=

# PostHog
NEXT_PUBLIC_POSTHOG_KEY=
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=development
```

After creating `.env.example`:
- Copy to `.env.local`
- **PAUSE EXECUTION** and prompt user: "Please fill in your .env.local file with the required credentials"
- Wait for user confirmation before proceeding

### 4. Clerk Authentication Setup (Use @context7 for latest docs)
- Install: `@clerk/nextjs`
- **Search Clerk documentation** using context7 for latest setup patterns
- Create `src/providers/clerk-provider.tsx` wrapping ClerkProvider
- Set up middleware in `src/middleware.ts`:
  - Integrate Clerk's `clerkMiddleware` or `authMiddleware`
  - Combine with locale detection for i18n
  - Protect routes appropriately (dashboard routes require auth)
- Create auth utilities in `src/lib/auth/`:
  - `currentUser.ts` - Get current user server-side
  - `protect.ts` - Route protection helpers
- Set up Clerk webhook handler at `src/app/api/webhooks/clerk/route.ts`:
  - Handle `user.created`, `user.updated`, `user.deleted` events
  - Sync user data to database
- Install shadcn auth components:
  - Run: `npx shadcn@latest add login-03`
  - Run: `npx shadcn@latest add signup-05`
- Create sign-in page at `src/app/[locale]/auth/sign-in/page.tsx` using login-03
- Create sign-up page at `src/app/[locale]/auth/sign-up/page.tsx` using signup-05
- Add `<UserButton />` component in dashboard layout
- Create `src/components/auth/` with:
  - `protected-route.tsx` - Client-side protection wrapper
  - `auth-guard.tsx` - Server component guard

### 5. Drizzle ORM Setup (with Postgres)
- Install: `drizzle-orm`, `drizzle-kit`, `postgres`
- Create `src/lib/db/index.ts` with connection setup
- Create `src/lib/db/schema.ts` with:
  - Users table (synced with Clerk)
  - Include `clerkId` field for linking
  - Example additional tables
- Set up `drizzle.config.ts`
- Create migration scripts in `package.json`
- Generate initial migration
- Add helper functions for Clerk user sync

### 6. Stripe Integration
- Install: `stripe`, `@stripe/stripe-js`
- Create `src/lib/stripe/client.ts` for client-side Stripe
- Create `src/lib/stripe/server.ts` for server-side operations
- Set up webhook handler at `src/app/api/webhooks/stripe/route.ts`
- Link Stripe customers to Clerk users via `clerkId`
- Create example checkout session API route
- Add Stripe provider in `src/providers/stripe-provider.tsx`

### 7. Resend Email Setup (Use context7 for latest docs)
- Install: `resend`, `react-email`
- **Search Resend documentation** using @context7
- Create `src/lib/email/index.ts`:
  - Initialize Resend client
  - Create `sendEmail()` utility function
  - Add email templates helpers
- Create `src/lib/email/templates/` with React Email templates:
  - `welcome.tsx` - Welcome email
  - `notification.tsx` - Generic notification
- Create API route `src/app/api/send-email/route.ts` for sending emails
- Add email sending to Clerk webhook (welcome email on user creation)
- Create type-safe email functions

### 8. PostHog Analytics Setup (Use context7 for latest docs)
- Install: `posthog-js`
- **Search PostHog NextJS documentation** using @context7
- Create `src/providers/posthog-provider.tsx`:
  - Initialize PostHog with proper NextJS configuration
  - Handle user identification with Clerk userId
  - Set up event autocapture
- Create `src/hooks/use-posthog.ts` for easy event tracking
- Add PostHog pageview tracking
- Set up feature flags support
- Create `src/lib/analytics/` with:
  - `events.ts` - Type-safe event tracking functions
  - `identify.ts` - User identification helpers
- Add PostHog to root layout
- Integrate with Clerk: identify users automatically on sign-in

### 9. Localization (i18n)
Implement a simple, file-based i18n approach:
- Create `src/lib/i18n/` directory
- Create translation JSON files:
  - `src/lib/i18n/locales/en.json`
  - `src/lib/i18n/locales/ar.json` (or user's preferred languages)
- Create `src/lib/i18n/index.ts` with translation utility functions
- Update `src/middleware.ts` to combine:
  - Clerk authentication middleware
  - Locale detection and routing
- Set up `[locale]` dynamic route in app directory
- **Next.js 15**: In layouts/pages using `params`, type it as `Promise<{ locale: string }>` and `await params` before accessing properties
- Create `useTranslation` hook in `src/hooks/use-translation.ts`
- Support RTL for Arabic/Hebrew if needed
- Translate auth pages and components

### 10. Shadcn UI Setup
- Initialize shadcn: `npx shadcn@latest init`
- Install sidebar: `npx shadcn@latest add sidebar-07`
- Install auth components:
  - `npx shadcn@latest add login-03`
  - `npx shadcn@latest add signup-05`
- Install essential components: 
  - `button`, `card`, `input`, `form`, `toast`, `dialog`
  - `avatar`, `dropdown-menu`, `separator`
  - `badge`, `tabs`, `skeleton`
- Configure theme in `tailwind.config.ts`
- Set up global styles in `src/app/globals.css`
- Create dashboard layout with sidebar-07 at `src/app/[locale]/dashboard/layout.tsx`:
  - Put `SidebarProvider`, `AppSidebar`, and `SidebarInset` in layout.tsx ONLY
  - Add user profile section with Clerk UserButton
  - Configure sidebar items (Dashboard, Settings, etc.)
  - Make sidebar responsive

### 11. Component Preview Page
Create `src/app/[locale]/preview/page.tsx`:
- **Purpose**: Showcase all custom components from `components/shared/` ONLY
- **Layout**: Organized sections for each component
- **Features**:
  - Display all variants of each component
  - Show component props and usage examples
  - Include code snippets for copy-paste
  - Add dark/light mode toggle
  - Make it visually appealing for UX testing
- **Structure**:
```tsx
  - Header with title "Component Preview"
  - Search/filter components
  - Grid/list of components
  - Each component card shows:
    - Component name
    - All variants
    - Props table
    - Code snippet (collapsible)
    - Live interactive demo
```
- Create `src/components/preview/` utilities:
  - `component-showcase.tsx` - Wrapper for each component demo
  - `code-block.tsx` - Syntax highlighted code display
  - `props-table.tsx` - Display component props
- Protect with auth (optional based on user preference)
- Add example shared components to demonstrate:
  - `src/components/shared/data-table.tsx`
  - `src/components/shared/stats-card.tsx`
  - `src/components/shared/page-header.tsx`

### 12. Additional Setup
- Create `src/providers/index.tsx` combining all providers:
  - ClerkProvider (outermost)
  - PostHogProvider
  - StripeProvider
  - Any other providers
- Set up root layout with proper provider nesting

## Key Principles
- Use TypeScript strictly throughout
- Implement proper error handling
- Add loading states where appropriate
- Follow NextJS 15+ App Router conventions
- Use server components by default, client components only when needed
- Implement proper type safety with Drizzle
- Add comments for complex logic
- Keep authentication flow simple, secure, and user-friendly
- Make preview page a valuable development tool

## Deliverables
1. Fully configured NextJS application with App Router
2. Complete Clerk authentication (sign-in, sign-up, protection, webhooks)
3. Working database connection with user sync
4. Stripe integration with authenticated users
5. Resend email sending capability with templates
6. PostHog analytics with user tracking
7. Multi-language support with simple i18n
8. Sidebar navigation using sidebar-07
9. Shadcn UI components ready to use (including auth components)
10. Component preview page for testing and development