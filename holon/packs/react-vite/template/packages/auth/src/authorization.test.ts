import { describe, expect, it } from "vitest";

import { isAuthorized } from "./authorization";
import type { AuthIdentity } from "./types";

const identity: AuthIdentity = {
  id: "person-1",
  displayName: "Template Maintainer",
  email: undefined,
  avatarUrl: undefined,
  roles: ["editor", "maintainer"],
  groups: ["platform"],
  claims: {},
};

describe("isAuthorized", () => {
  it("rejects anonymous access", () => {
    expect(isAuthorized(null)).toBe(false);
  });

  it("accepts any matching role by default", () => {
    expect(isAuthorized(identity, { roles: ["admin", "editor"] })).toBe(true);
  });

  it("supports all-role and group requirements", () => {
    expect(
      isAuthorized(identity, {
        roles: ["editor", "maintainer"],
        groups: ["platform"],
        requireAllRoles: true,
      }),
    ).toBe(true);
  });
});
