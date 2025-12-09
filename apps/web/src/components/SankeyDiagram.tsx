import { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

interface SankeyNode {
  sourceLayer: string;
  language: string;
  violationType: string;
  fixTarget: string;
  count?: number;
}

interface SankeyDiagramProps {
  data: SankeyNode[];
}

export default function SankeyDiagram({ data }: SankeyDiagramProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current && data.length > 0) {
      // Generate Sankey diagram from data
      const sankeyChart = generateSankeyChart(data);
      // Security: Use mermaid.render for safer rendering with unique IDs
      const id = `sankey-${Date.now()}-${Math.random().toString(36).substring(2, 11)}`;
      mermaid.render(id, sankeyChart).then(({ svg }) => {
        if (ref.current) {
          ref.current.innerHTML = svg;
        }
      }).catch(err => {
        console.error('Sankey diagram rendering error:', err);
        if (ref.current) {
          ref.current.textContent = 'Error rendering diagram';
        }
      });
    }
  }, [data]);

  return (
    <div className="w-full overflow-x-auto">
      <div ref={ref} className="mermaid min-w-[600px]" />
    </div>
  );
}

function sanitizeString(str: string): string {
  // Security: Escape dangerous characters while preserving valid Mermaid syntax
  // Only escape characters that could lead to XSS or syntax breaking
  return String(str)
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function generateSankeyChart(data: SankeyNode[]): string {
  // Group by source layer, language, and fix target
  const flows = data.map(node => {
    const count = node.count || 1;
    // Security: Sanitize all user-provided strings to prevent XSS
    // Note: Mermaid with strict security level provides additional protection
    const source = sanitizeString(node.sourceLayer);
    const language = sanitizeString(node.language);
    const violation = sanitizeString(node.violationType);
    const target = sanitizeString(node.fixTarget);
    
    return `${source},${language},${count}\n${language},${violation},${count}\n${violation},${target},${count}`;
  }).join('\n');

  return `
%%{init: {'theme':'dark', 'themeVariables': { 'primaryColor': '#3b82f6', 'primaryTextColor': '#fff', 'primaryBorderColor': '#1e40af', 'lineColor': '#64748b', 'secondaryColor': '#1e293b', 'tertiaryColor': '#0f172a'}}}%%
sankey-beta

${flows}
  `.trim();
}
