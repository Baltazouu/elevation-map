import {Flex, Heading, HStack} from "@chakra-ui/react"

export default function Navbar() {

  return (
    <Flex
      w="100%"
      h={54}
      px="4"
      py="5"
      align="center"
      justify="flex-start"
      className="app-navbar"
    >

      <HStack>
        <Heading pl={4}>Elevation Map</Heading>
      </HStack>

    </Flex>
  )
}