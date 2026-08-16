export type AuthenticationStatus = "anonymous" | "authenticating" | "authenticated" | "error";

export interface AuthIdentity {
  id: string;
  displayName: string;
  email: string | undefined;
  avatarUrl: string | undefined;
  roles: readonly string[];
  groups: readonly string[];
  /** Provider claims retained for advanced consumers without coupling the core API. */
  claims: Readonly<Record<string, unknown>>;
}

export interface AuthState {
  status: AuthenticationStatus;
  identity: AuthIdentity | null;
  accessToken: string | undefined;
  error: Error | undefined;
}

export interface AuthAdapter {
  getState(): AuthState;
  getServerState?(): AuthState;
  subscribe(listener: () => void): () => void;
  signIn(options?: Readonly<Record<string, unknown>>): Promise<void>;
  signOut(options?: Readonly<Record<string, unknown>>): Promise<void>;
  refresh?(): Promise<void>;
}

export interface AuthorizationRequirement {
  roles?: readonly string[];
  groups?: readonly string[];
  requireAllRoles?: boolean;
  requireAllGroups?: boolean;
}
