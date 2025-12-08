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
      ref.current.innerHTML = sankeyChart;
      mermaid.contentLoaded();
    }
  }, [data]);

  return (
    <div className="w-full overflow-x-auto">
      <div ref={ref} className="mermaid min-w-[600px]" />
    </div>
  );
}

function generateSankeyChart(data: SankeyNode[]): string {
  // Group by source layer, language, and fix target
  const flows = data.map(node => {
    const count = node.count || 1;
    const source = `${node.sourceLayer}`;
    const language = `${node.language}`;
    const violation = node.violationType;
    const target = node.fixTarget;
    
    return `${source},${language},${count}\n${language},${violation},${count}\n${violation},${target},${count}`;
  }).join('\n');

  return `
%%{init: {'theme':'dark', 'themeVariables': { 'primaryColor': '#3b82f6', 'primaryTextColor': '#fff', 'primaryBorderColor': '#1e40af', 'lineColor': '#64748b', 'secondaryColor': '#1e293b', 'tertiaryColor': '#0f172a'}}}%%
sankey-beta

${flows}
  `.trim();
}
