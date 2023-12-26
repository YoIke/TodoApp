"use client";

import React from "react";
import {
  Box,
  Flex,
  Heading,
  Button,
  Text,
  useColorMode,
  IconButton,
} from "@chakra-ui/react";
import { useRouter } from "next/navigation";
import { MdBrightness4, MdBrightness7, MdExitToApp } from "react-icons/md";

// usernameをpropsとして受け取る
const Header: React.FC<{ username?: string }> = ({ username }) => {
  const { colorMode, toggleColorMode } = useColorMode();
  const router = useRouter();
  // ログアウト処理
  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:8001/logout", {
        method: "POST",
        credentials: "include",
      });

      if (response.ok) {
        // レスポンスが成功した場合、ログインページにリダイレクト
        router.push("/login");
      } else {
        // エラー処理
        console.error("Logout failed");
      }
    } catch (error) {
      console.error("Error during logout", error);
    }
  };
  return (
    <Box bg="teal.500" w="100%" p={4} color="white">
      <Flex alignItems="center" justifyContent="space-between">
        <Flex alignItems="center">
          <Heading as="h1" size="lg" mr={4}>
            池田勉強アプリケーション
          </Heading>
          {username && <Text fontSize="md">こんにちは, {username}</Text>}
        </Flex>
        <Flex>
          <IconButton
            icon={colorMode === "light" ? <MdBrightness4 /> : <MdBrightness7 />}
            onClick={toggleColorMode}
            aria-label="Toggle color mode"
            mr={2}
          />
          <IconButton
            icon={<MdExitToApp />}
            onClick={handleLogout}
            aria-label="Logout"
          />
        </Flex>
      </Flex>
    </Box>
  );
};

export default Header;
