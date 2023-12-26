"use client";

import React, { useState, useEffect } from "react";
import { redirect } from "next/navigation";
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
import { useRouter } from "next/navigation";

function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();
  const [errorMessage, setErrorMessage] = useState("");
  const checkAuthStatus = async () => {
    try {
      const response = await fetch("http://localhost:8001/check-auth", {
        credentials: "include",
      });
      if (response.ok) {
        const data = await response.json();
        if (data.isAuthenticated) {
          router.push("/top");
        }
      }
    } catch (error) {
      console.error("認証状態のチェック中にエラー", error);
    }
  };
  useEffect(() => {
    checkAuthStatus();
  }, []);
  const handleSubmit = async (event: { preventDefault: () => void }) => {
    event.preventDefault();

    try {
      const response = await fetch("http://localhost:8001/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include", // クッキーを含める
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      console.log(data);

      if (response.ok) {
        router.push("./top");
      } else {
        // レスポンスが 'ok' でない場合、エラーメッセージを設定
        setErrorMessage("ログインに失敗しました: " + data.error);
      }
    } catch (error) {
      console.error("ログインエラー", error);
      setErrorMessage("ログイン処理中にエラーが発生しました");
    }
  };

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
          <form onSubmit={handleSubmit}>
            <VStack spacing={4}>
              <FormControl id="email">
                <FormLabel>Email address</FormLabel>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </FormControl>
              <FormControl id="password">
                <FormLabel>Password</FormLabel>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </FormControl>
              <Button width="full" mt={4} type="submit">
                Sign In
              </Button>
              {errorMessage && (
                <Box color="red.500" textAlign="center" my={2}>
                  {errorMessage}
                </Box>
              )}
            </VStack>
          </form>
        </Box>
      </Center>
    </ChakraProvider>
  );
}

export default LoginForm;
