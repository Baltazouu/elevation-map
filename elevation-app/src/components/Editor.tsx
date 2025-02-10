import { useState } from "react";
import { FormControl, FormLabel, Select, VStack, Button } from "@chakra-ui/react";
import { getGpx } from "../service/api/CallGpx";

interface EditorProps {
  onTrackDataReceived: (gpxString: string) => void;
}

export const Editor: React.FC<EditorProps> = ({ onTrackDataReceived }) => {
  const [elevation, setElevation] = useState<number>(100);
  const [distance, setDistance] = useState<number>(10);
  const [isLoading, setIsLoading] = useState<boolean>(false); // State pour gérer le loader

  const handleElevationChanged = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setElevation(Number(event.target.value));
  };

  const handleDistanceChanged = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setDistance(Number(event.target.value));
  };

  const submit = async () => {
    setIsLoading(true); // Déclenche le loader
    try {
      const gpxString = await getGpx(distance, elevation);
      if (gpxString) {
        onTrackDataReceived(gpxString);
      }
    } catch (error) {
      console.error("Erreur lors de la récupération du GPX :", error);
    } finally {
      setIsLoading(false); // Cache le loader après l'exécution
    }
  };

  return (
    <VStack padding={8} spacing={8}>
      <FormControl>
        <FormLabel>Distance (km)</FormLabel>
        <Select value={distance} onChange={handleDistanceChanged}>
          <option value='10'>10</option>
          <option value='25'>25</option>
          <option value='40'>40</option>
          <option value='50'>50</option>
          <option value='60'>60</option>
        </Select>
      </FormControl>

      <FormControl>
        <FormLabel>Dénivelé (m)</FormLabel>
        <Select value={elevation} onChange={handleElevationChanged}>
          <option value='100'>100</option>
          <option value='300'>300</option>
          <option value='600'>600</option>
          <option value='800'>800</option>
          <option value='1200'>1200</option>
        </Select>
      </FormControl>

      <Button onClick={submit} isLoading={isLoading} loadingText="Chargement..." colorScheme="teal" variant="solid">
        Submit
      </Button>
    </VStack>
  );
};

export default Editor;
