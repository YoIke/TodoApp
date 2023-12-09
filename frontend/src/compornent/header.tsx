"use client";

import React from "react";
import { Box, Flex, Heading, Button, useColorMode } from "@chakra-ui/react";

const Header: React.FC = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  return (
    <Box bg="teal.500" w="100%" p={4} color="white">
      <Flex alignItems="center" justifyContent="space-between">
        <Heading as="h1" size="lg">
          アプリケーション名
        </Heading>
        <Button onClick={toggleColorMode}>
          {colorMode === "light" ? "ダークモード" : "ライトモード"}
        </Button>
      </Flex>
    </Box>
  );
};

export default Header;
