/**
 * Environment variable utilities for SynergyMesh contracts-l1 service.
 * Provides type-safe access to required environment variables with fail-fast behavior.
 */

/**
 * 取得必要的環境變數 (Get required environment variable)
 *
 * Retrieves a required environment variable by name.
 * Throws an error immediately if the variable is not set,
 * enabling fail-fast behavior during application startup.
 *
 * @param name - The name of the environment variable to retrieve
 * @returns The value of the environment variable
 * @throws {Error} When the environment variable is not set
 *
 * @example
 * // Get a required environment variable
 * const apiKey = getRequiredEnv('API_KEY');
 */
export function getRequiredEnv(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`Environment variable ${name} is not set.`);
  }

  return value;
}

/**
 * 取得 WE_TONKE token (Get WE_TONKE token)
 *
 * Retrieves the WE_TONKE environment variable which contains
 * a token/API key used for authentication or authorization.
 * This function should be called during application startup
 * to ensure the required token is available.
 *
 * @returns The WE_TONKE token value
 * @throws {Error} When WE_TONKE environment variable is not set
 *
 * @example
 * // During application startup
 * const token = getWeTonke();
 * // Use token for API calls or authentication
 */
export function getWeTonke(): string {
  return getRequiredEnv('WE_TONKE');
}

/**
 * 取得選填的環境變數 (Get optional environment variable)
 *
 * Retrieves an optional environment variable by name.
 * Returns undefined if the variable is not set.
 *
 * @param name - The name of the environment variable to retrieve
 * @returns The value of the environment variable, or undefined if not set
 *
 * @example
 * // Get an optional environment variable with fallback
 * const debugMode = getOptionalEnv('DEBUG_MODE') ?? 'false';
 */
export function getOptionalEnv(name: string): string | undefined {
  return process.env[name];
}

/**
 * 驗證所有必要的環境變數 (Validate all required environment variables)
 *
 * Validates that all specified environment variables are set.
 * This function is useful for validating multiple variables at once
 * during application startup.
 *
 * @param names - Array of environment variable names to validate
 * @returns Object containing all validated environment variable values
 * @throws {Error} When any of the specified environment variables is not set
 *
 * @example
 * // Validate multiple required environment variables
 * const env = validateRequiredEnvs(['DATABASE_URL', 'API_KEY', 'WE_TONKE']);
 * console.log(env.DATABASE_URL, env.API_KEY, env.WE_TONKE);
 */
export function validateRequiredEnvs(names: string[]): Record<string, string> {
  const result: Record<string, string> = {};

  for (const name of names) {
    result[name] = getRequiredEnv(name);
  }

  return result;
}
