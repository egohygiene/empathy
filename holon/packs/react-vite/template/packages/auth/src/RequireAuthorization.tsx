import type { ReactNode } from "react";

import { useAuth } from "./AuthProvider";
import type { AuthorizationRequirement } from "./types";

export interface RequireAuthorizationProps extends AuthorizationRequirement {
  children: ReactNode;
  fallback?: ReactNode;
}

export function RequireAuthorization({
  children,
  fallback = null,
  roles,
  groups,
  requireAllRoles,
  requireAllGroups,
}: RequireAuthorizationProps) {
  const auth = useAuth();
  const requirement: AuthorizationRequirement = {};

  if (roles !== undefined) {
    requirement.roles = roles;
  }
  if (groups !== undefined) {
    requirement.groups = groups;
  }
  if (requireAllRoles !== undefined) {
    requirement.requireAllRoles = requireAllRoles;
  }
  if (requireAllGroups !== undefined) {
    requirement.requireAllGroups = requireAllGroups;
  }

  return auth.isAuthorized(requirement) ? children : fallback;
}
