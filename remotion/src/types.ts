export type Caption = {
  text: string;
  startFrame: number;
  endFrame: number;
};

export type VideoInput = {
  title: string;
  imagePaths: string[];
  captions: Caption[];
  durationInFrames: number;
};
