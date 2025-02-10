import {useState} from "react";
import {TrackData} from "../model/TrackData";
import {Map} from "./Map";
import Editor from "./Editor";
import {downloadFile} from "../service/Util";
import {Button, Flex, Grid, GridItem, Spacer} from "@chakra-ui/react";
import {GpxParser} from "../service/GpxParser";
import VideoMapContext from "../context/VideoMapContext";

const DURATION_IN_SEC = 20;
const START_BEARING = 0;

export const VideoMap: React.FC = () => {
  const [trackData, setTrackData] = useState<TrackData | null>(null);
  const [keySetting] = useState<number>(0);
  const [duration, setDuration] = useState<number>(DURATION_IN_SEC);
  const [bearing, setBearing] = useState<number>(START_BEARING);
  const [is3DEnabled, setIs3DEnabled] = useState<boolean>(true);
  const [isFlyOnPointEnabled, setIsFlyOnPointEnabled] = useState<boolean>(true);
  const [videoBlob, setVideoBlob] = useState<Blob | null>(null);

  const handleTrackDataReceived = (gpxString: string) => {
    const gpxParser = new GpxParser();
    const parsedData = gpxParser.parse(gpxString);
    setTrackData(parsedData);
  };

  const downloadVideo = () => downloadFile(`${trackData?.name}.webm`, videoBlob);

  const contextState = {
    trackData,
    duration,
    bearing,
    is3DEnabled,
    isFlyOnPointEnabled,
    setDuration,
    setBearing,
    setIs3DEnabled,
    setVideoBlob,
    setIsFlyOnPointEnabled,
  };

  return (
    <VideoMapContext.Provider value={contextState}>
      <Grid gridTemplateColumns={'350px 1fr'}>
        <GridItem w='100%' h={"94vh"} className="map-editor" boxShadow='lg'>
          <Flex direction={'column'} justifyContent={'center'} alignItems={'center'} height="100%" padding={4}>
            <Editor onTrackDataReceived={handleTrackDataReceived} />
            <Spacer />
            {trackData && (
              <Button backgroundColor={'#677357'} onClick={downloadVideo}
                isLoading={videoBlob == null}
                isDisabled={trackData == null}
                loadingText='Processing video'>
                Download Video
              </Button>
            )}
          </Flex>
        </GridItem>

        {trackData && <GridItem w='100%' h={"94vh"}><Map key={keySetting} /></GridItem>}
      </Grid>
    </VideoMapContext.Provider>
  );
};

export default VideoMap;
