import {FormControl, FormLabel, Input, Select, VStack} from "@chakra-ui/react";
import VideoMapContext from "../context/VideoMapContext";
import {ChangeEvent, useContext} from "react";

const MIN_DURATION_IN_SEC = 5;



export const Editor: React.FC = () => {

  const {
    duration, setDuration,
    bearing, setBearing
  } = useContext(VideoMapContext);

  const handleDurationChange = (e: ChangeEvent<HTMLInputElement>) => setDuration(parseInt(e.target.value));
  const handleBearingChanged = (e) => setBearing(parseInt(e.target.value));


  return (
    <VStack padding={8} spacing={8}>

      <FormControl>
        <FormLabel>Dénivelé (m)</FormLabel>
        <Select value={bearing} onChange={handleBearingChanged}>
          <option value='300'>300</option>
          <option value='600'>300</option>
          <option value='800'>800</option>
          <option value='1200'>1200</option>
        </Select>
      </FormControl>

      <FormControl>
        <FormLabel>Distance (km)</FormLabel>
        <Select value={bearing} onChange={handleBearingChanged}>
          <option value='25'>25</option>
          <option value='40'>40</option>
          <option value='50'>50</option>
          <option value='60'>60</option>
        </Select>
      </FormControl>

    </VStack>
  )
}

export default Editor;
