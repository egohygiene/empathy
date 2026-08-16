import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useSyncExternalStore,
  type ReactNode,
} from "react";

import { isAuthorized } from "./authorization";
import type { AuthAdapter, AuthState, AuthorizationRequirement } from "./types";

export interface AuthContextValue extends AuthState {
  signIn(options?: Readonly<Record<string, unknown>>): Promise<void>;
  signOut(options?: Readonly<Record<string, unknown>>): Promise<void>;
  refresh(): Promise<void>;
  isAuthorized(requirement?: AuthorizationRequirement): boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export interface AuthProviderProps {
  adapter: AuthAdapter;
  children: ReactNode;
}

export function AuthProvider({ adapter, children }: AuthProviderProps) {
  const state = useSyncExternalStore(
    adapter.subscribe,
    adapter.getState,
    adapter.getServerState ?? adapter.getState,
  );
  const authorize = useCallback(
    (requirement: AuthorizationRequirement = {}) => isAuthorized(state.identity, requirement),
    [state.identity],
  );
  const refresh = useCallback(async () => {
    await adapter.refresh?.();
  }, [adapter]);
  const signIn = useCallback(
    async (options?: Readonly<Record<string, unknown>>) => adapter.signIn(options),
    [adapter],
  );
  const signOut = useCallback(
    async (options?: Readonly<Record<string, unknown>>) => adapter.signOut(options),
    [adapter],
  );
  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      signIn,
      signOut,
      refresh,
      isAuthorized: authorize,
    }),
    [authorize, refresh, signIn, signOut, state],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider.");
  }

  return context;
}

export function useHasRole(...roles: readonly string[]): boolean {
  return useAuth().isAuthorized({ roles });
}

export function useHasGroup(...groups: readonly string[]): boolean {
  return useAuth().isAuthorized({ groups });
}
