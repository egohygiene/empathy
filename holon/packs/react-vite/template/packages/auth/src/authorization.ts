import type { AuthIdentity, AuthorizationRequirement } from "./types";

function includesRequired(
  actual: readonly string[],
  required: readonly string[],
  requireAll: boolean,
): boolean {
  if (required.length === 0) {
    return true;
  }

  return requireAll
    ? required.every((value) => actual.includes(value))
    : required.some((value) => actual.includes(value));
}

export function isAuthorized(
  identity: AuthIdentity | null,
  requirement: AuthorizationRequirement = {},
): boolean {
  if (!identity) {
    return false;
  }

  const roles = requirement.roles ?? [];
  const groups = requirement.groups ?? [];

  return (
    includesRequired(identity.roles, roles, requirement.requireAllRoles ?? false) &&
    includesRequired(identity.groups, groups, requirement.requireAllGroups ?? false)
  );
}
