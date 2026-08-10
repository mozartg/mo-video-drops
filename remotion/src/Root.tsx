import { Composition } from "remotion";
import { DriveOutComposition } from "./DriveOutComposition";
import { longFormInput, trialInput } from "./input";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="DriveOutTrial"
        component={DriveOutComposition}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={trialInput}
      />
      <Composition
        id="DriveOutLongForm"
        component={DriveOutComposition}
        durationInFrames={18000}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={longFormInput}
      />
    </>
  );
};
