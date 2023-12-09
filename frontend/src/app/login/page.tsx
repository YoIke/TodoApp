import {
  Box,
  Button,
  Center,
  ChakraProvider,
  FormControl,
  FormLabel,
  Input,
  VStack,
} from "@chakra-ui/react";

function LoginForm() {
  return (
    <ChakraProvider>
      <Center h="100vh">
        <Box
          p={8}
          maxWidth="500px"
          borderWidth={1}
          borderRadius={8}
          boxShadow="lg"
        >
          <VStack spacing={4}>
            <FormControl id="email">
              <FormLabel>Email address</FormLabel>
              <Input type="email" />
            </FormControl>
            <FormControl id="password">
              <FormLabel>Password</FormLabel>
              <Input type="password" />
            </FormControl>
            <Button width="full" mt={4} type="submit">
              Sign In
            </Button>
          </VStack>
        </Box>
      </Center>
    </ChakraProvider>
  );
}

export default LoginForm;
