import { Button, Input, Label, PageHeader, SectionCard, UsageMeter } from '@repo/ui';

import { DisplayAccessState } from '../../../features/feature-access/display-access-state';
import { resolveFeatureAccess } from '../../../features/feature-access/resolve-access';

export default function VideoDownloaderPage() {
  const access = resolveFeatureAccess('video.downloader', 'anonymous');

  return (
    <div className="space-y-6">
      <PageHeader
        description="Freemium public video downloader placeholder. No download is executed in this phase."
        title="Video Downloader"
      />
      <SectionCard title="Download placeholder">
        <form className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="video-url">Video URL</Label>
            <Input id="video-url" placeholder="https://example.com/video" type="url" />
          </div>
          <Button type="button">Prepare download</Button>
        </form>
      </SectionCard>
      <SectionCard title="Access and quota">
        <div className="space-y-4">
          <DisplayAccessState access={access} />
          <UsageMeter label="Guest daily quota" value={0} />
          <p className="text-sm text-muted-foreground">
            Login or upgrade placeholders will unlock history, batch, quality, and paid options.
          </p>
        </div>
      </SectionCard>
    </div>
  );
}
