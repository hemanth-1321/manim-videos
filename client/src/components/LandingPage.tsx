import { TextArea } from "./TextArea";
import VideoGallery from "./VideoGallery";

export function LandingPage() {
  return (
    <div className="h-screen">
      <section className="h-3/6 flex items-center justify-center">
        <TextArea />
      </section>
      <section className="h-2/5">
<VideoGallery/>
      </section>
    </div>
  );
}
