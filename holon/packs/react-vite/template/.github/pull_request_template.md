## Summary

<!-- Explain the outcome and the ownership boundary it changes. -->

## Validation

- [ ] `pnpm run check:workspace`
- [ ] `pnpm run typecheck`
- [ ] `pnpm run test`
- [ ] `pnpm run build`
- [ ] Relevant app/profile smoke-tested

## Template impact

- [ ] Staging promotion/removal is recorded in the migration ledger.
- [ ] New behavior is core only when every consumer needs it; otherwise it is opt-in.
- [ ] `VITE_*` values contain no secrets.
- [ ] Documentation and examples use long-form CLI arguments.
