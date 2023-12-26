"use client";

import React from "react";
import Header from "@/compornent/header";
import { useRouter } from "next/navigation";
import useSWR from "swr";

const fetcher = (url: string) =>
  fetch(url, { credentials: "include" }).then((res) => res.json());

function useAuth() {
  const { data, error } = useSWR("http://localhost:8001/check-auth", fetcher);
  return {
    user: data,
    isLoading: !error && !data,
    isError: error,
  };
}

const Template = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter();
  const { user, isLoading, isError } = useAuth();

  React.useEffect(() => {
    // データがロードされた後、認証されていない場合にリダイレクト
    if (!isLoading && !user?.isAuthenticated) {
      router.push("/login");
    }
  }, [router, user, isLoading]);

  // ローディング中の表示
  if (isLoading) return <div>ローディング中...</div>;
  // エラーが発生した場合の表示
  if (isError) return <div>エラーが発生しました。</div>;
  console.log(user);
  // 認証されたユーザーのコンテンツを表示
  return (
    <div>
      <Header username={user.username} />
      {children}
    </div>
  );
};

export default Template;
