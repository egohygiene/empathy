import type { AuthAdapter, AuthIdentity, AuthState } from "./types";

export interface MemoryAuthAdapterOptions {
  initialIdentity?: AuthIdentity | null;
  signedInIdentity: AuthIdentity;
  latencyMs?: number;
}

const delay = async (milliseconds: number): Promise<void> => {
  if (milliseconds <= 0) {
    return;
  }

  await new Promise<void>((resolve) => {
    globalThis.setTimeout(resolve, milliseconds);
  });
};

/**
 * Development and test adapter. It intentionally does not manufacture a token;
 * tests that exercise authenticated API calls must provide a dedicated adapter.
 */
export function createMemoryAuthAdapter(options: MemoryAuthAdapterOptions): AuthAdapter {
  const listeners = new Set<() => void>();
  const initialIdentity = options.initialIdentity ?? null;
  let state: AuthState = {
    status: initialIdentity ? "authenticated" : "anonymous",
    identity: initialIdentity,
    accessToken: undefined,
    error: undefined,
  };

  const publish = (nextState: AuthState): void => {
    state = nextState;
    listeners.forEach((listener) => listener());
  };

  return {
    getState: () => state,
    getServerState: () => state,
    subscribe: (listener) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    signIn: async () => {
      publish({ ...state, status: "authenticating", error: undefined });
      await delay(options.latencyMs ?? 0);
      publish({
        status: "authenticated",
        identity: options.signedInIdentity,
        accessToken: undefined,
        error: undefined,
      });
    },
    signOut: async () => {
      await delay(options.latencyMs ?? 0);
      publish({
        status: "anonymous",
        identity: null,
        accessToken: undefined,
        error: undefined,
      });
    },
  };
}
