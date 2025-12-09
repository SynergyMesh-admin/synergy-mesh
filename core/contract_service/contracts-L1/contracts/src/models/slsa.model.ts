/**
 * SLSA Models and Validation Schemas
 * Centralized data models for SLSA attestation operations
 */

import { z } from 'zod';

// ==================== Validation Schemas ====================

/**
 * Schema for creating SLSA attestation
 */
export const createAttestationSchema = z
  .object({
    subjectPath: z.string().optional(),
    subjectDigest: z.string().optional(),
    subjectName: z.string().optional(),
    buildType: z.string().default('https://synergymesh.dev/contracts/build/v1'),
    builder: z.object({
      id: z.string().min(1, 'Builder ID is required'),
      version: z.string().min(1, 'Builder version is required'),
    }),
  })
  .refine(
    (data) =>
      Boolean(data.subjectPath) || (Boolean(data.subjectDigest) && Boolean(data.subjectName)),
    {
      message: 'Either subjectPath or both subjectDigest and subjectName must be provided',
    }
  );

/**
 * Schema for verifying attestation
 */
export const verifyAttestationSchema = z.object({
  provenance: z.any().refine((val) => val !== undefined && val !== null, {
    message: 'Provenance is required',
  }),
});

/**
 * Schema for generating digest
 */
export const generateDigestSchema = z.object({
  content: z.string().min(1, 'Content is required'),
});

// ==================== TypeScript Types ====================

/**
 * Infer TypeScript types from Zod schemas
 */
export type CreateAttestationInput = z.infer<typeof createAttestationSchema>;
export type VerifyAttestationInput = z.infer<typeof verifyAttestationSchema>;
export type GenerateDigestInput = z.infer<typeof generateDigestSchema>;
