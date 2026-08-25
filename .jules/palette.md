## 2025-02-23 - Replaced jarring native alert() with inline feedback
**Learning:** Native `alert()` calls for simple actions like copying to clipboard are jarring and interrupt user flow. Providing inline feedback directly on the button is a much smoother and modern UX pattern. Adding `aria-label`s to copy buttons significantly improves screen reader accessibility.
**Action:** Always prefer inline feedback over `alert()` for non-critical information or simple actions. Ensure all icon-only or simple text buttons have appropriate `aria-label`s.
