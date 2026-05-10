---
version: alpha
name: Primer Executive Tasks
description: A high-end task app using GitHub Primer-inspired foundations translated into Google's DESIGN.md token format.
colors:
  primary: "#0D1117"
  secondary: "#57606A"
  tertiary: "#0969DA"
  neutral: "#F6F8FA"
  canvas: "#FFFFFF"
  success: "#1A7F37"
  danger: "#CF222E"
  border: "#D0D7DE"
typography:
  h1:
    fontFamily: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 3rem
    fontWeight: 760
    lineHeight: 1.02
    letterSpacing: "-0.055em"
  h2:
    fontFamily: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 1.25rem
    fontWeight: 720
    lineHeight: 1.2
  body-md:
    fontFamily: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 1rem
    fontWeight: 450
    lineHeight: 1.55
  label:
    fontFamily: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 0.78rem
    fontWeight: 760
    lineHeight: 1
    letterSpacing: "0.08em"
rounded:
  sm: 8px
  md: 14px
  lg: 24px
  xl: 32px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.md}"
    padding: 12px
  card:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
    padding: 24px
---

## Overview

This design file is based on the reputable, open GitHub Primer design system foundations (`https://primer.style/foundations/`) and encoded with Google's DESIGN.md spec. The app should feel like a premium GitHub-native productivity surface: precise, calm, spacious, and developer-trustworthy.

## Colors

- **Primary (#0D1117):** GitHub dark canvas ink for strong contrast and executive polish.
- **Tertiary (#0969DA):** Primer blue for the single high-emphasis action path.
- **Neutral (#F6F8FA):** soft background that keeps cards crisp.
- **Success/Danger:** reserved for completion and destructive affordances.

## Typography

Use system UI with Inter-style proportions. Headlines are compact and high confidence; labels are all-caps and sparse.

## Layout

Use generous spacing, a centered max-width shell, layered cards, and a dashboard-like two-column composition on desktop. Mobile collapses to a single stacked flow.

## Elevation & Depth

Depth comes from subtle borders, high-radius cards, and soft blue/black shadows rather than heavy gradients.

## Shapes

Rounded cards and pill controls should feel modern but not playful. Avoid sharp enterprise boxes.

## Components

Primary buttons are blue, full-confidence actions. Todo rows are cards with a visible ownership boundary and soft status treatments.

## Do's and Don'ts

- Do keep the interface sparse, readable, and premium.
- Do make auth and multi-user state obvious.
- Don't use toy colors, emoji-heavy UI, or generic Bootstrap defaults.
