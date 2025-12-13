# Tailwind UI Illustrations

Create polished, interactive landing page illustrations using Tailwind CSS and React. Build dashboard previews, hero sections with tab-based screenshots, and interactive UI mockups that showcase SaaS products.

## When to Use

Use this skill when creating:
- Landing page hero sections with dashboard previews
- Interactive sidebar + content layouts
- Tab-based feature showcases
- Demo components that show real app functionality
- Marketing illustrations that need to feel "alive"

## Core Philosophy

**Don't fake it with rectangles - make it real.**

Landing page illustrations should mirror actual app experiences:
- Real text labels (not lorem ipsum or gray boxes)
- Actual data structures with realistic sample values
- Interactive elements that demonstrate functionality
- Production-quality Tailwind styling

---

## Pattern 1: Interactive Dashboard Layout

A sidebar + content area where clicking sidebar items changes the main content.

### Structure

```
┌─────────────────────────────────────────┐
│ Outer Container (relative positioning)  │
│ ┌─────────┬───────────────────────────┐ │
│ │ Sidebar │ Content Area              │ │
│ │ (fixed) │ (data table/content)      │ │
│ │         │                           │ │
│ └─────────┴───────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Implementation

```tsx
'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'

type ActiveView = 'dashboard' | 'analytics' | 'settings'

// Sample data - use realistic values for your domain
const dashboardData = [
    { name: 'Project Alpha', status: 'Active', progress: '78%', updated: '2h ago' },
    { name: 'Project Beta', status: 'Review', progress: '95%', updated: '1d ago' },
    { name: 'Project Gamma', status: 'Draft', progress: '23%', updated: '3d ago' },
]

export const DashboardIllustration = () => {
    const [activeView, setActiveView] = useState<ActiveView>('dashboard')

    return (
        <div aria-hidden className="relative">
            {/* Floating content panel */}
            <div className="absolute -right-48 bottom-2 md:-right-4 md:bottom-6 md:left-[13rem] md:w-[calc(100%-12rem)]">
                {activeView === 'dashboard' && <DashboardTable />}
                {activeView === 'analytics' && <AnalyticsTable />}
                {activeView === 'settings' && <SettingsPanel />}
            </div>

            <div className="mask-b-from-50% rounded-2xl border overflow-hidden">
                {/* Sidebar */}
                <div className="absolute inset-y-0 left-0 w-[12rem] border-r bg-gray-50 text-[11px]">
                    {/* Logo header */}
                    <div className="flex items-center gap-1.5 border-b border-gray-100 px-3 py-2.5">
                        <div className="size-4 rounded bg-gray-900" />
                        <span className="font-semibold text-gray-900">Your App</span>
                    </div>

                    {/* Navigation items */}
                    <div className="px-2.5 py-2">
                        <div className="mb-1.5 text-[10px] font-medium text-gray-400 px-1.5">Navigation</div>
                        <div className="space-y-0.5">
                            {(['dashboard', 'analytics', 'settings'] as const).map((view) => (
                                <button
                                    key={view}
                                    onClick={() => setActiveView(view)}
                                    className={cn(
                                        "flex h-6 w-full items-center gap-1.5 rounded-md px-1.5 transition-colors capitalize",
                                        activeView === view
                                            ? "bg-gray-200 font-medium text-gray-900"
                                            : "text-gray-600 hover:bg-gray-100"
                                    )}>
                                    <span>{view}</span>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Main content area background */}
                <div className="ml-auto w-[calc(100%-12rem)]">
                    <div className="h-11 border-b" />
                    <div className="relative h-80">
                        <div className="absolute inset-0 bg-[repeating-linear-gradient(-45deg,var(--color-border),var(--color-border)_1px,transparent_1px,transparent_6px)] opacity-50" />
                    </div>
                </div>
            </div>
        </div>
    )
}
```

### Sidebar Button Pattern

```tsx
<button
    onClick={() => setActiveView('dashboard')}
    className={cn(
        "flex h-6 w-full items-center gap-1.5 rounded-md px-1.5 transition-colors",
        activeView === 'dashboard'
            ? "bg-gray-200 font-medium text-gray-900"
            : "text-gray-600 hover:bg-gray-100"
    )}>
    <svg className="size-3" /* icon */ />
    <span>Dashboard</span>
</button>
```

### Data Table Pattern

```tsx
const DataTable = ({ className }: { className?: string }) => (
    <div className={cn(
        'bg-background ring-foreground/7 relative mx-auto max-w-4xl rounded-2xl border border-transparent p-6 shadow-md shadow-black/5 ring-1',
        className
    )}>
        <div className="mb-4">
            <div className="font-medium">Table Title</div>
            <p className="text-muted-foreground mt-0.5 text-sm">Description of what this data shows</p>
        </div>
        <table className="w-full table-auto border-collapse">
            <thead className="bg-foreground/[0.02]">
                <tr className="*:border *:border-foreground/7 *:p-3 *:text-sm *:font-medium">
                    <th className="rounded-l-md text-left">Name</th>
                    <th className="text-center">Status</th>
                    <th className="rounded-r-md text-center">Value</th>
                </tr>
            </thead>
            <tbody className="text-sm">
                {data.map((item, i) => (
                    <tr key={i} className="*:border *:border-foreground/7 *:p-2">
                        <td className="font-medium">{item.name}</td>
                        <td className="text-center">{item.status}</td>
                        <td className="tabular-nums text-center">{item.value}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
)
```

---

## Pattern 2: Hero Section with Tab-based Screenshots

A hero section where tabs switch between different dashboard screenshots.

### Structure

```
┌─────────────────────────────────────────┐
│           Badge (optional)              │
│              Headline                   │
│            Subheadline                  │
│         [CTA] [Secondary CTA]           │
│                                         │
│   ┌─────┐   ┌─────┐   ┌─────┐          │
│   │ Tab │   │ Tab │   │ Tab │          │
│   └─────┘   └─────┘   └─────┘          │
│ ┌─────────────────────────────────────┐ │
│ │      Dashboard Screenshot           │ │
│ │       (switches on tab click)       │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Implementation

```tsx
'use client'

import Image from 'next/image'
import { useState } from 'react'
import { cn } from '@/lib/utils'
import { AnimatePresence, motion } from 'motion/react'
import { LayoutDashboard, BarChart3, Settings } from 'lucide-react'

type Preview = 'dashboard' | 'analytics' | 'settings'

const previews = [
    { name: 'dashboard' as const, label: 'Dashboard', image: '/screenshots/dashboard.png', icon: <LayoutDashboard /> },
    { name: 'analytics' as const, label: 'Analytics', image: '/screenshots/analytics.png', icon: <BarChart3 /> },
    { name: 'settings' as const, label: 'Settings', image: '/screenshots/settings.png', icon: <Settings /> },
]

export const HeroIllustration = () => {
    const [active, setActive] = useState<Preview>('dashboard')
    const currentPreview = previews.find((p) => p.name === active)!

    return (
        <div className="relative pt-12 lg:pt-24">
            <div className="mx-auto max-w-6xl">
                {/* Tab switcher */}
                <div className="grid grid-cols-[1fr_auto_1fr] border-y border-foreground/7 pb-2">
                    {/* Decorative side patterns */}
                    <div className="h-[calc(100%+0.5rem)] bg-[repeating-linear-gradient(45deg,var(--color-foreground),var(--color-foreground)_1px,transparent_1px,transparent_6px)] opacity-[0.04]" />

                    {/* Tab buttons */}
                    <div className="bg-background">
                        <div className="grid grid-cols-3 items-center gap-px divide-x divide-foreground/7 border-x border-foreground/7 *:h-16">
                            {previews.map((preview) => (
                                <button
                                    key={preview.name}
                                    onClick={() => setActive(preview.name)}
                                    className="group flex cursor-pointer items-center justify-center px-2">
                                    <div className={cn(
                                        'ring-foreground/7 flex h-10 items-center gap-2 rounded-full px-4 ring-1 transition-all duration-150 [&>svg]:size-4',
                                        active === preview.name
                                            ? 'bg-background shadow shadow-black/10'
                                            : 'group-hover:bg-foreground/[0.02]'
                                    )}>
                                        {preview.icon}
                                        <span className="hidden md:inline">{preview.label}</span>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="h-[calc(100%+0.5rem)] bg-[repeating-linear-gradient(45deg,var(--color-foreground),var(--color-foreground)_1px,transparent_1px,transparent_6px)] opacity-[0.04]" />
                </div>
            </div>

            {/* Screenshot container */}
            <div className="relative mx-auto -mt-2 max-w-6xl pb-16 lg:px-10 lg:pb-20">
                <div className="w-full rounded-2xl overflow-hidden shadow-[0_8px_60px_-12px_rgba(0,0,0,0.15)] ring-1 ring-black/[0.04]">
                    <AnimatePresence mode="popLayout" initial={false}>
                        <motion.div
                            key={active}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.15 }}>
                            <Image
                                className="w-full h-auto block"
                                src={currentPreview.image}
                                alt={currentPreview.label}
                                width={2880}
                                height={1920}
                                sizes="(max-width: 640px) 768px, (max-width: 1024px) 1280px, 1280px"
                            />
                        </motion.div>
                    </AnimatePresence>
                </div>
            </div>
        </div>
    )
}
```

---

## Styling Reference

### Color Scheme

```tsx
// Backgrounds
'bg-gray-50'           // Sidebar background
'bg-background'        // Content area
'bg-foreground/[0.02]' // Table header

// Borders
'border-gray-100'      // Light dividers
'border-foreground/7'  // Subtle borders

// Text
'text-gray-900'        // Primary text
'text-gray-600'        // Secondary text
'text-gray-400'        // Muted text

// Interactive states
'hover:bg-gray-100'    // Hover background
'bg-gray-200'          // Active state
```

### Shadow Patterns

```tsx
// Card shadow
'shadow-md shadow-black/5 ring-1 ring-foreground/7'

// Screenshot container shadow
'shadow-[0_8px_60px_-12px_rgba(0,0,0,0.15)] ring-1 ring-black/[0.04]'
```

### Decorative Patterns

```tsx
// Diagonal stripe background
'bg-[repeating-linear-gradient(45deg,var(--color-foreground),var(--color-foreground)_1px,transparent_1px,transparent_6px)] opacity-[0.04]'

// Crosshatch pattern
'bg-[repeating-linear-gradient(-45deg,var(--color-border),var(--color-border)_1px,transparent_1px,transparent_6px)] opacity-50'
```

### Status Badge Colors

```tsx
<span className={cn(
    'inline-flex px-2 py-0.5 rounded-full text-[10px] font-medium',
    status === 'Active' && 'bg-emerald-50 text-emerald-700',
    status === 'Pending' && 'bg-amber-50 text-amber-700',
    status === 'Inactive' && 'bg-red-50 text-red-700',
)}>{status}</span>
```

---

## Inline SVG Icons

Keep illustrations self-contained with inline SVGs:

```tsx
// Plus icon
<svg className="size-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
</svg>

// Search icon
<svg className="size-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
</svg>

// Chart icon
<svg className="size-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
</svg>

// Folder icon
<svg className="size-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
</svg>

// Users icon
<svg className="size-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
</svg>

// Star icon (filled)
<svg className="size-3 text-amber-400 fill-amber-400" viewBox="0 0 24 24">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
</svg>
```

---

## Checklist

Before finishing an illustration component:

- [ ] Uses `'use client'` directive (required for useState)
- [ ] Has `aria-hidden` on decorative containers
- [ ] Uses actual text labels, not placeholder rectangles
- [ ] Interactive elements have hover/active states
- [ ] Data looks realistic (proper formatting, believable values)
- [ ] Icons are appropriately sized (`size-3` for small, `size-4` for medium)
- [ ] Matches Tailwind color conventions
- [ ] Mobile-responsive (test at different breakpoints)
- [ ] Smooth transitions on state changes

---

## Dependencies

This skill assumes a Next.js + Tailwind CSS project with:

```json
{
  "dependencies": {
    "react": "^18",
    "next": "^14",
    "tailwindcss": "^3",
    "motion": "^11",
    "lucide-react": "^0.400",
    "clsx": "^2",
    "tailwind-merge": "^2"
  }
}
```

The `cn()` utility combines clsx and tailwind-merge:

```ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```
