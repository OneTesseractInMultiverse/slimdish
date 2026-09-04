import { ProgressBar, Tile } from '@carbon/react';
import type { Widget } from '../services/dashboard';

type WidgetCardProps = Readonly<{ widget: Widget }>;

function percentage(value: string): number {
  const parsed = Number.parseInt(value.replace('%', ''), 10);
  return Number.isNaN(parsed) ? 0 : Math.min(100, Math.max(0, parsed));
}

export function WidgetCard({ widget }: WidgetCardProps) {
  return (
    <Tile className="widget-card">
      <p className="widget-card__label">{widget.title}</p>
      <p className="widget-card__value">{widget.value}</p>
      {widget.kind === 'progress' ? (
        <ProgressBar label={widget.detail} value={percentage(widget.value)} />
      ) : (
        <p className="widget-card__detail">{widget.detail}</p>
      )}
    </Tile>
  );
}

