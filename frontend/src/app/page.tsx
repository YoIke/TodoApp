import { redirect } from "next/navigation";

function Home() {
  redirect("./login");
  return <>ホーム</>;
}

export default Home;
