import {useRef} from "react";
import {Button, Flex, Heading, HStack} from "@chakra-ui/react";
import pako from "pako";
import {addGpx} from "../service/api/CallGpx";

export default function Navbar() {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      console.log("Fichier sélectionné :", file);

      try {

        const fileText = await file.text();
        const fileBytes = new TextEncoder().encode(fileText);
        const gzippedData = pako.gzip(fileBytes);
        await addGpx(gzippedData);

      } catch (error) {
        console.error("Erreur lors de la compression du fichier :", error);
      }
    }
  };

  return (
    <Flex
      w="100%"
      h={75}
      px={4}
      align="center"
      direction="row"
      justify="space-between"
      className="app-navbar"
    >
      <HStack>
        <Heading pl={4}>Elevation Map</Heading>
      </HStack>

      <Button colorScheme="teal" variant="solid" onClick={handleButtonClick}>
        Add GPX
      </Button>

      {/* Input de fichier caché */}
      <input
        type="file"
        ref={fileInputRef}
        accept=".gpx"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
    </Flex>
  );
}
