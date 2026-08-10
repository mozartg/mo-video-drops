import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { parseVideoInput } from "./input";
import type { VideoInput } from "./types";

const sceneColors = ["#0b132b", "#1c2541", "#3a506b"];

const assetUrl = (path: string): string => staticFile(path.replace(/\\/g, "/"));

const CaptionTrack: React.FC<{ captions: VideoInput["captions"] }> = ({ captions }) => {
  const frame = useCurrentFrame();
  const activeCaption = captions.find(
    (caption) => frame >= caption.startFrame && frame < caption.endFrame,
  );

  if (!activeCaption) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        left: 64,
        right: 64,
        bottom: 120,
        padding: "24px 28px",
        borderRadius: 22,
        backgroundColor: "rgba(3, 7, 18, 0.84)",
        color: "#ffffff",
        fontFamily: "Arial, sans-serif",
        fontSize: 42,
        fontWeight: 700,
        lineHeight: 1.16,
        textAlign: "center",
      }}
    >
      {activeCaption.text}
    </div>
  );
};

const Scene: React.FC<{
  index: number;
  path: string;
  durationInFrames: number;
  title: string;
}> = ({ index, path, durationInFrames, title }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: sceneColors[index % sceneColors.length] }}>
      <Img
        src={assetUrl(path)}
        alt={title}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: interpolate(
            frame,
            [0, 20, Math.max(20, durationInFrames - 20), durationInFrames],
            [0.72, 1, 1, 0.78],
            {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.16, 1, 0.3, 1),
            },
          ),
          scale: interpolate(frame, [0, durationInFrames], [1, 1.06], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      />
      <AbsoluteFill
        style={{
          background: "linear-gradient(180deg, rgba(4, 8, 20, 0.18) 0%, rgba(4, 8, 20, 0.8) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};

export const DriveOutComposition: React.FC<VideoInput> = (rawInput) => {
  const input = parseVideoInput(rawInput);
  const sceneDuration = Math.ceil(input.durationInFrames / input.imagePaths.length);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0b132b" }}>
      {input.imagePaths.map((path, index) => {
        const from = index * sceneDuration;
        const durationInFrames = Math.min(sceneDuration, input.durationInFrames - from);

        return (
          <Sequence
            key={path}
            from={from}
            durationInFrames={durationInFrames}
            layout="absolute-fill"
          >
            <Scene
              index={index}
              path={path}
              durationInFrames={durationInFrames}
              title={input.title}
            />
          </Sequence>
        );
      })}
      <div
        style={{
          position: "absolute",
          top: 72,
          left: 64,
          right: 64,
          color: "#ffffff",
          fontFamily: "Arial, sans-serif",
          fontSize: 28,
          fontWeight: 700,
          letterSpacing: 1.6,
          textTransform: "uppercase",
        }}
      >
        {input.title}
      </div>
      <CaptionTrack captions={input.captions} />
    </AbsoluteFill>
  );
};
