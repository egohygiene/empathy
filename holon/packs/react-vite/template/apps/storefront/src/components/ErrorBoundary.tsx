import { Component, type ErrorInfo, type ReactNode } from "react";

interface ErrorBoundaryProps {
  readonly children: ReactNode;
}

interface ErrorBoundaryState {
  readonly error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  override state: ErrorBoundaryState = {
    error: null,
  };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  override componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error("Unhandled storefront error", {
      error,
      errorInfo,
    });
  }

  override render(): ReactNode {
    if (this.state.error) {
      return (
        <main className="error-boundary">
          <section className="error-boundary__content">
            <p className="error-boundary__eyebrow">Storefront error</p>

            <h1>Something went wrong</h1>

            <p>The store encountered an unexpected problem. Refresh the page and try again.</p>

            <button
              type="button"
              onClick={() => {
                window.location.reload();
              }}
            >
              Refresh page
            </button>
          </section>
        </main>
      );
    }

    return this.props.children;
  }
}
