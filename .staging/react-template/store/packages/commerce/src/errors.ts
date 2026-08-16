export class CommerceError extends Error {
  readonly status?: number;
  readonly code: string;

  constructor(message: string, options?: { status?: number; code?: string; cause?: unknown }) {
    super(message, { cause: options?.cause });
    this.name = "CommerceError";
    this.status = options?.status;
    this.code = options?.code ?? "commerce_error";
  }
}
