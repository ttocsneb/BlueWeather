interface PluginItem {
  human_name: string;
  description: string;
  author: string;
  url: string;
  entrypoints: Array<string>;
  builtin: boolean;
  enabled: boolean;
  disableable: boolean;
}
type PluginList = {[key: string]: PluginItem}
interface PluginResponse {
  plugins: PluginList;
  page: number;
  items: number;
  pages: number;
  total: number;
}
