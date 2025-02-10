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
        <FormLabel>Dénivelé</FormLabel>
        <Input type='number' min={MIN_DURATION_IN_SEC} value={duration} onChange={handleDurationChange} />
      </FormControl>

      <FormControl>
        <FormLabel>Distance</FormLabel>
        <Select value={bearing} onChange={handleBearingChanged}>
          <option value='0'>North</option>
          <option value='90'>East</option>
          <option value='180'>South</option>
          <option value='270'>West</option>
        </Select>
      </FormControl>


    </VStack>
  )
}

export default Editor;
