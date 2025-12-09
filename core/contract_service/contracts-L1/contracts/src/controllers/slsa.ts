import { Request, Response } from 'express';

import { formatZodError, isZodError } from '../middleware/zodErrorHandler';
import {
  slsaCreateAttestationSchema,
  slsaVerifyAttestationSchema,
  slsaGenerateDigestSchema,
} from '../models/slsa.model';
import { SLSAAttestationService } from '../services/attestation';

export class SLSAController {
  private slsaService: SLSAAttestationService;

  constructor() {
    this.slsaService = new SLSAAttestationService();
  }

  /**
   * 創建 SLSA 構建溯源認證
   */
  createAttestation = async (req: Request, res: Response): Promise<void> => {
    try {
      const validatedInput = slsaCreateAttestationSchema.parse(req.body);

      let subjects;
      if (validatedInput.subjectPath) {
        // 從文件路徑創建主體
        const fs = await import('fs/promises');
        const content = await fs.readFile(validatedInput.subjectPath);
        subjects = [this.slsaService.createSubjectFromContent(validatedInput.subjectPath, content)];
      } else {
        // 從摘要創建主體
        subjects = [
          this.slsaService.createSubjectFromDigest(
            validatedInput.subjectName!,
            validatedInput.subjectDigest!.replace('sha256:', '')
          ),
        ];
      }

      const metadata = this.slsaService.generateContractBuildMetadata(
        validatedInput.subjectName || validatedInput.subjectPath || 'unknown',
        '1.0.0',
        'synergymesh-contracts-l1'
      );

      // 更新構建元數據
      metadata.builder.id = validatedInput.builder.id;
      metadata.builder.version = {
        builder: validatedInput.builder.version,
        node: process.version,
      };
      metadata.buildType = validatedInput.buildType;
      metadata.finishedOn = new Date().toISOString();

      const provenance = await this.slsaService.createProvenance(subjects, metadata);

      res.status(201).json({
        success: true,
        data: {
          provenance,
          attestationId: metadata.invocationId,
          subjects: subjects.length,
          buildType: metadata.buildType,
        },
        message: 'SLSA build provenance attestation created successfully',
      });
    } catch (error) {
      if (isZodError(error)) {
        res.status(400).json({
          success: false,
          error: formatZodError(error),
          timestamp: new Date().toISOString(),
        });
        return;
      }
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to create SLSA attestation',
        timestamp: new Date().toISOString(),
      });
    }
  };

  /**
   * 驗證 SLSA 認證
   */
  verifyAttestation = async (req: Request, res: Response): Promise<void> => {
    try {
      const { provenance } = slsaVerifyAttestationSchema.parse(req.body);

      const isValid = await this.slsaService.verifyProvenance(provenance);

      res.json({
        success: true,
        data: {
          valid: isValid,
          timestamp: new Date().toISOString(),
          provenanceType:
            typeof provenance === 'object' && provenance !== null && 'predicateType' in provenance
              ? (provenance as { predicateType: string }).predicateType
              : 'unknown',
        },
        message: isValid ? 'SLSA attestation is valid' : 'SLSA attestation is invalid',
      });
    } catch (error) {
      if (isZodError(error)) {
        res.status(400).json({
          success: false,
          error: formatZodError(error),
          timestamp: new Date().toISOString(),
        });
        return;
      }
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to verify SLSA attestation',
        timestamp: new Date().toISOString(),
      });
    }
  };

  /**
   * 從內容生成摘要
   */
  generateDigest = async (req: Request, res: Response): Promise<void> => {
    try {
      const { content } = slsaGenerateDigestSchema.parse(req.body);

      const subject = this.slsaService.createSubjectFromContent(
        'user-content',
        Buffer.from(content, 'utf-8')
      );

      res.json({
        success: true,
        data: {
          subject: subject.name,
          digest: subject.digest,
          sha256: subject.digest.sha256,
          algorithm: 'sha256',
          timestamp: new Date().toISOString(),
        },
        message: 'Digest generated successfully',
      });
    } catch (error) {
      if (isZodError(error)) {
        res.status(400).json({
          success: false,
          error: formatZodError(error),
          timestamp: new Date().toISOString(),
        });
        return;
      }
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to generate digest',
        timestamp: new Date().toISOString(),
      });
    }
  };

  /**
   * 生成合約部署的認證
   */
  createContractAttestation = async (req: Request, res: Response): Promise<void> => {
    try {
      const { contractName, contractVersion, deployerAddress, contractCode, deploymentTxHash } =
        req.body;

      if (!contractName || !contractCode) {
        res.status(400).json({
          success: false,
          error: 'Contract name and code are required',
          timestamp: new Date().toISOString(),
        });
        return;
      }

      const subject = this.slsaService.createSubjectFromContent(
        `${contractName}.sol`,
        Buffer.from(contractCode, 'utf-8')
      );

      const metadata = this.slsaService.generateContractBuildMetadata(
        contractName,
        contractVersion || '1.0.0',
        deployerAddress || 'unknown'
      );

      metadata.buildType = 'https://synergymesh.dev/contracts/deployment/v1';
      metadata.externalParameters = {
        ...metadata.externalParameters,
        deploymentTxHash,
        contractName,
        deployerAddress,
      };
      metadata.finishedOn = new Date().toISOString();

      const provenance = await this.slsaService.createProvenance([subject], metadata);

      res.status(201).json({
        success: true,
        data: {
          provenance,
          contractAttestation: {
            contractName,
            contractVersion,
            deployerAddress,
            deploymentTxHash,
            codeHash: subject.digest.sha256,
            attestationId: metadata.invocationId,
          },
        },
        message: 'Contract deployment attestation created successfully',
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to create contract attestation',
        timestamp: new Date().toISOString(),
      });
    }
  };

  /**
   * 獲取認證摘要資訊
   */
  getAttestationSummary = async (req: Request, res: Response): Promise<void> => {
    try {
      const { provenance } = req.body;

      if (!provenance) {
        res.status(400).json({
          success: false,
          error: 'Provenance data is required',
          timestamp: new Date().toISOString(),
        });
        return;
      }

      const isValid = await this.slsaService.verifyProvenance(provenance);

      const summary = {
        valid: isValid,
        type: provenance.predicateType || 'unknown',
        subjects: provenance.subject?.length || 0,
        subjectNames: provenance.subject?.map((s: { name?: string }) => s.name) || [],
        buildType: provenance.predicate?.buildDefinition?.buildType || 'unknown',
        builder: provenance.predicate?.runDetails?.builder?.id || 'unknown',
        timestamp: provenance.predicate?.runDetails?.metadata?.startedOn || 'unknown',
        invocationId: provenance.predicate?.runDetails?.metadata?.invocationId || 'unknown',
      };

      res.json({
        success: true,
        data: summary,
        message: 'Attestation summary generated successfully',
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to generate attestation summary',
        timestamp: new Date().toISOString(),
      });
    }
  };
}
