import type { Caption, VideoInput } from "./types";

const DEFAULT_TRIAL_DURATION = 450;
const DEFAULT_LONG_FORM_DURATION = 18000;

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null;

const isSafeAssetPath = (value: string): boolean => {
  if (value.includes("..") || value.includes(":")) {
    return false;
  }

  return !value.startsWith("/") && !value.startsWith("\\");
};

const parseCaption = (value: unknown): Caption => {
  if (!isRecord(value) || typeof value.text !== "string") {
    throw new Error("Each caption must include text, startFrame, and endFrame");
  }

  const { startFrame, endFrame } = value;
  if (
    typeof startFrame !== "number" ||
    typeof endFrame !== "number" ||
    !Number.isInteger(startFrame) ||
    !Number.isInteger(endFrame) ||
    startFrame < 0 ||
    endFrame <= startFrame
  ) {
    throw new Error("Caption frames must be non-negative integers with endFrame after startFrame");
  }

  return { text: value.text, startFrame, endFrame };
};

export const parseVideoInput = (value: unknown): VideoInput => {
  if (!isRecord(value) || typeof value.title !== "string" || !value.title.trim()) {
    throw new Error("Video input requires a non-empty title");
  }

  if (
    !Array.isArray(value.imagePaths) ||
    value.imagePaths.length < 3 ||
    value.imagePaths.some(
      (path) => typeof path !== "string" || !path.trim() || !isSafeAssetPath(path),
    )
  ) {
    throw new Error("Video input requires at least three safe repository-relative image paths");
  }

  if (!Array.isArray(value.captions)) {
    throw new Error("Video input requires a caption track");
  }

  const durationInFrames = value.durationInFrames ?? DEFAULT_TRIAL_DURATION;
  if (
    typeof durationInFrames !== "number" ||
    !Number.isInteger(durationInFrames) ||
    durationInFrames <= 0
  ) {
    throw new Error("durationInFrames must be a positive integer");
  }

  const captions = value.captions.map(parseCaption);
  for (const caption of captions) {
    if (caption.endFrame > durationInFrames) {
      throw new Error("Caption endFrame must be within the video duration");
    }
  }

  return {
    title: value.title,
    imagePaths: value.imagePaths,
    captions,
    durationInFrames,
  };
};

export const trialInput: VideoInput = parseVideoInput({
  title: "Drive Out: Keep Your Receipts",
  imagePaths: [
    "trial-assets/drive-out-poster.png",
    "trial-assets/drive-out-poster-2.png",
    "trial-assets/sample-shots.png",
  ],
  captions: [
    { text: "Track the work. Keep the proof.", startFrame: 0, endFrame: 135 },
    { text: "Drive Out is built for the miles between the app and the bank.", startFrame: 135, endFrame: 300 },
    { text: "Start with the receipts you already own.", startFrame: 300, endFrame: 450 },
  ],
  durationInFrames: DEFAULT_TRIAL_DURATION,
});

export const longFormInput: VideoInput = parseVideoInput({
  title: "Drive Out: The Work Behind the Wheel",
  imagePaths: trialInput.imagePaths,
  captions: [
    { text: "The long route starts with a clear record.", startFrame: 0, endFrame: 1800 },
    { text: "Every scene is driven by the same JSON contract.", startFrame: 1800, endFrame: 5400 },
    { text: "Keep the story useful, specific, and grounded.", startFrame: 5400, endFrame: 9000 },
    { text: "A durable workflow turns finished clips into a destination.", startFrame: 9000, endFrame: 12600 },
    { text: "Drive Out: know the work, keep the proof.", startFrame: 12600, endFrame: DEFAULT_LONG_FORM_DURATION },
  ],
  durationInFrames: DEFAULT_LONG_FORM_DURATION,
});
